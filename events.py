from flask_socketio import emit
from app import socketio
messages = []
@socketio.on('connect')
def handle_connect():
    emit("messages", messages)


@socketio.on('messages')
def handle_messages():
    print('DDDDDDDDDDDDD')
    emit("messages", messages)


@socketio.on("message")
def handle_message(message: str):
    messages.append(message)
    emit('message', message, broadcast=True)

