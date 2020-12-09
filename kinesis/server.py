from os import urandom
from flask import Flask, render_template
from flask.app import g
from flask_socketio import SocketIO, send, emit
from kinesis_api import DynamoDbAPI
from time import sleep

stocks = ["AAPL", "GOOGL", "NVDA", "FB", "QCOM", "MSFT", "AMZN", "NFLX", "TSLA", "INTC"]
DYNAMO_DB_TABLE = "stock-stream-data"
DYNAMO_DB_PARTITION_KEY = "symbol"
SYNAMO_DB_SORT_KEY = "minute"


app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(32).hex
app.config["THREADED"] = True
app.config["DEBUG"] = True

socketio = SocketIO(app)

db = None


def setup_db():
    global db
    db = DynamoDbAPI(table_name=DYNAMO_DB_TABLE)


app.before_first_request(setup_db)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect", namespace="/api/socket.io")
def on_connect():
    print("SocketIO: Connected!")


@socketio.on_error(namespace="/api/socket.io")
def error_handler(err):
    print(f"ERROR: {err}")


@socketio.on("get_graph_data", namespace='/api/socket.io')
def get_graph_data(symbol):
    print("Stock Symbol:", symbol)

    resp = db.get_all(
        filter="symbol = :stock",
        expr_attr_values={":stock": symbol}
    )

    if resp["status_code"] == 200:
        emit(
            "graph_data",
            {"symbol": symbol, "data": resp["items"]},
            json=True,
            namespace="/api/socket.io"
        )
        sleep(60.0)


@socketio.on("disconnect", namespace="/api/socket.io")
def on_disconnect():
    print("SocketIO: Disconnected!")


if __name__ == "__main__":
    socketio.run(app)
