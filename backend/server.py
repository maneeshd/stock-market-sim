from os import urandom, path
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from kinesis_api import DynamoDbAPI
from time import sleep
import pandas as pd


CUR_DIR = path.realpath(path.dirname(__file__))
DYNAMO_DB_TABLE = "stock-stream-data"
DYNAMO_DB_PARTITION_KEY = "symbol"
SYNAMO_DB_SORT_KEY = "minute"


app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(32).hex
app.config["THREADED"] = True
app.config["DEBUG"] = True
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

db = DynamoDbAPI(table_name=DYNAMO_DB_TABLE)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/get_historical_data")
def get_historical_data():
    stock = request.args.get("stock")
    file_ = path.join(CUR_DIR, "data", f"hist-{stock}.csv")
    df = pd.read_csv(file_, index_col=0)
    return jsonify(df.to_dict(orient="records"))


@socketio.on("connect", namespace="/api/socket.io")
def on_connect():
    print("SocketIO: Connected!")


@socketio.on_error(namespace="/api/socket.io")
def error_handler(err):
    print(f"ERROR: {err}")


@socketio.on("get_live_data", namespace='/api/socket.io')
def get_live_data(symbol):
    print("Stock Symbol:", symbol)

    resp = db.get_all(
        projection_expr="symbol, #m, #o",
        expr_attr_names={"#m": "minute", "#o": "open"},
        filter="symbol = :stock",
        expr_attr_values={":stock": symbol}
    )

    labels = []
    data = []
    for item in resp["items"]:
        labels.append(item["minute"]["S"])
        data.append(float(item["open"]["N"]))

    emit(
        "graph_data",
        {"symbol": symbol, "labels": labels, "data": data},
        json=True,
        namespace="/api/socket.io"
    )
    sleep(60.0)


@socketio.on("disconnect", namespace="/api/socket.io")
def on_disconnect():
    print("SocketIO: Disconnected!")


if __name__ == "__main__":
    socketio.run(app)
