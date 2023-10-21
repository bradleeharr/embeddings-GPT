from flask import Flask, render_template
from flask_socketio import SocketIO
from chat import handle_message

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message_event(msg):
    response = handle_message(msg)
    socketio.emit('response', response)


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
