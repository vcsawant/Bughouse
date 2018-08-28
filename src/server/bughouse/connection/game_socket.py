from flask_socketio import send, emit
import logging
from bughouse import socketio

LOGGER = logging.getLogger(__name__)
GAME_NAMESPACE = "/game"


@socketio.on_error(namespace=GAME_NAMESPACE)
def handle_game_error(exc):
    LOGGER.exception("Error in game socket")
    pass


@socketio.on('message', namespace=GAME_NAMESPACE)
def handle_message_in_game(data):
    return True
