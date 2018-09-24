from flask_socketio import emit
from chess import Move
import logging
from bughouse import socketio, db
from flask_socketio import Namespace, join_room, leave_room
from flask_login import current_user
import bughouse.utils as utils
import sys

LOGGER = logging.getLogger(__name__)
GAME_NAMESPACE = "/game"


@socketio.on_error_default
def default_error_handler(err):
    LOGGER.exception('error has occurred\t', err)


class GameNamespace(Namespace):
    def on_connect(self):
        if current_user.is_authenticated:
            return True
        else:
            return False

    def on_disconnect(self):
        LOGGER.info(current_user.name + " disconnected")
        pass

    def on_view(self):
        join_room(room='__view')

    def on_join(self, data):
        game_id = data.get('game_id', None)
        position = data.get('position', None)

        if game_id is None or position is None:
            raise KeyError('invalid join game request')

        try:
            game = utils.get_game_from_id(game_id)
            game.add_player(current_user, position)
            db.session.commit()
            join_room(room=game_id, sid=current_user.id)
            leave_room(room='__view')
            emit('refresh', room='__view')

        except:
            # todo: exc handling
            LOGGER.error("Error adding player to game: " + sys.exc_info()[0])
            raise
        emit('status', {'message': current_user.id + ' has joined at position ' + position, 'status': 'join',
                        'position': position}, room=game_id)

    def on_move(self, data):
        game_id = data.get('game_id', None)
        move_uci = data.get('move', None)

        if game_id is None or move_uci is None:
            raise KeyError('invalid move')

        move = Move.from_uci(move_uci)
        # TODO: finish

    def on_test(self, data):
        game_id = data.get('game_id', None)
        message = data.get('message', None)

        if game_id is None or message is None:
            raise KeyError('invalid test')

        emit('test_response', {'message': message, 'sender': current_user.id}, room=game_id)


socketio.on_namespace(GameNamespace('/game'))
