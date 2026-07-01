from flask import request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

from extensions import socketio


online_users = set()


@socketio.on("connect")
def handle_connect():

    if not current_user.is_authenticated:
        return False

    room = f"user_{current_user.id}"

    join_room(room)

    online_users.add(current_user.id)

    emit(
        "user_online",
        {
            "user_id": current_user.id
        },
        broadcast=True
    )

    print(
        f"{current_user.id} connected"
    )


@socketio.on("disconnect")
def handle_disconnect():

    if current_user.is_authenticated:

        room = f"user_{current_user.id}"

        leave_room(room)

        online_users.discard(
            current_user.id
        )

        emit(
            "user_offline",
            {
                "user_id": current_user.id
            },
            broadcast=True
        )

        print(
            f"{current_user.id} disconnected"
        )


@socketio.on("join_chat")
def join_chat(data):

    receiver_id = int(
        data["receiver_id"]
    )

    room = "_".join(
        map(
            str,
            sorted(
                [
                    current_user.id,
                    receiver_id
                ]
            )
        )
    )

    join_room(room)

    emit(
        "joined",
        {
            "room": room
        }
      )
