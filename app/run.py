import eventlet

eventlet.monkey_patch()

from flask_socketio import SocketIO, emit, join_room, leave_room, send
from create_app import create_app
from flask import request

from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import config
from models import SocketConnection, Notification
from database import create
from service import get_subscribed_users


sid = None

flask_app = create_app()
socketio = SocketIO(flask_app, engineio_logger=False, async_mode="eventlet")


@socketio.on("connect")
def connect():
    socketio.emit("connected-response", {"data": "Connected to server"})


@socketio.on("username")
def add_user_connection(msg):
    sid = request.sid
    create(SocketConnection({"username": msg, "connection_id": sid}))


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


def emit_notif():
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=config.KAFKA_1,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        consumer.subscribe(config.KAFKA_TOPIC)
    except KafkaError as err:
        print("kafka producer - Exception during connecting to broker - {}".format(err))
        return

    for message in consumer:
        post_owner = message.value["username"]
        with flask_app.app_context():
            users_to_notify = get_subscribed_users(post_owner)
            for user in users_to_notify:
                socketio.emit(
                    "new-post", data=json.dumps(message.value), to=user.connection_id
                )


if __name__ == "__main__":
    socketio.start_background_task(emit_notif)
    socketio.run(flask_app, host="0.0.0.0", port=8091)
