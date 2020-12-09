from os import urandom
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from kinesis_api import KinesisAPI
from time import sleep


app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(32).hex
app.config["THREADED"] = True
app.config["DEBUG"] = True

socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def on_connect():
    print("SocketIO: Connected!")


@socketio.on_error()
def error_handler(err):
    print(f"ERROR: {err}")


@socketio.on('message')
def handle_message(message):
    print("Received message:", message)
    for i in range(50):
        emit("graph_data", {"data": i + 1}, json=True)
        sleep(5)


@socketio.on("disconnect")
def on_disconnect(data=None):
    print("SocketIO: Disconnected!", f"Data: {data}")


if __name__ == "__main__":
    socketio.run(app)
