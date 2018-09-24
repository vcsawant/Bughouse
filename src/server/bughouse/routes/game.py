from bughouse.models import Game, Player, Board, GameSchema
from bughouse.models.game import BughouseMove
import chess
import bughouse.utils as utils
from flask import request, make_response, jsonify
import logging
from bughouse import app, db, socketio
import sys
from flask_socketio import join_room, leave_room
from flask_login import current_user, login_required

LOGGER = logging.getLogger(__name__)
GAME_NAMESPACE = "/game"


def parse_move(move_json):
    uci = move_json.get('uci', None)
    board_code = move_json.get('board', None)
    if (board_code is None) or (uci is None):
        raise KeyError('missing needed key')

    move = chess.Move.from_uci(uci)
    bughouse_move = BughouseMove(board_code, move)
    return bughouse_move


def validate_and_push_move(gameid, move):
    game = utils.get_game_from_id(gameid)

    if not game.validate_move(move):
        raise ValueError('invalid move')

    game.make_move(move)
    LOGGER.info("pushed move on board " + str(game.id) + "_" + move.board_code + ": " + move.move.uci())

    return True


@app.route("/game/<gameid>/move/", methods=["POST"])
@login_required
def move_a(gameid):
    try:
        move = parse_move(request.get_json(force=True))
        if validate_and_push_move(gameid, move):
            db.session.commit()

            return make_response('success', 200)
    except KeyError:
        LOGGER.exception('error parsing move', exc_info=sys.exc_info())
    except ValueError:
        LOGGER.exception('error validating move', exc_info=sys.exc_info())


@app.route("/game/view/<gameid>")
@login_required
def view(gameid):
    LOGGER.info("viewing board")
    game = utils.get_game_from_id(gameid)
    return game.board_a.board.fen() + " and " + game.board_b.board.fen()


@app.route("/game/create", methods=["POST"])
@login_required
def create_game():
    game = Game()
    db.session.add(game)
    db.session.commit()
    LOGGER.debug("created game with id " + str(game.id))
    return make_response(str(game.id), 201)


@app.route("/game/join/<game_id>", methods=["POST"])
@login_required
def add_player_to_game(game_id):
    game = utils.get_game_from_id(game_id)

    player_id = request.form['player_id']
    player = utils.get_player_from_id(player_id)
    position = request.get_json(force=True).get('position', None)
    try:
        game.add_player(player, position)
    except:
        # todo: exc handling
        LOGGER.error("Error adding player to game: " + sys.exc_info()[0])
        return make_response("Error adding player to game: " + jsonify(utils.game_schema.dump(game).data))

    try:
        db.session.commit()
    except:
        # todo: exc handling
        LOGGER.error("Error committing updated player: " + sys.exc_info()[0])
        raise

    try:
        join_room(room=game_id, namespace=GAME_NAMESPACE, sid=player_id)
    except Exception:
        LOGGER.exception("error joining game room")
        return make_response("Unable to join game", 505)
    return make_response("Joined game " + str(utils.game_schema.dump(game).data), 200)


@app.route("/game/view")
@login_required
def view_all_games():
    LOGGER.debug("viewing all games")
    games = Game.query.all()
    return jsonify(utils.games_schema.dump(games).data)


#################################################
#   DEBUG TOOLS                                 #
#################################################

@app.route("/debug/drop", methods=["POST"])
def drop_db():
    db.drop_all()
    return make_response("done", 200)


@app.route("/debug/game/<game_id>/finish", methods=["POST"])
def finish_game_and_update(game_id):
    game = utils.get_game_from_id(game_id)
    game.finish_game(0)
    db.session.commit()
    return make_response("ended game", 200)


@app.route("/debug/create", methods=["POST"])
def create_db():
    db.create_all()
    return make_response("done", 200)
