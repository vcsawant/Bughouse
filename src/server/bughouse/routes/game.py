from bughouse.models import Game, Player, Board, GameSchema
from bughouse.models.game import CustomMove
import chess
import bughouse.utils as utils
from flask import request, make_response, jsonify
import logging
from bughouse import app, db, socketio
import sys
from flask_socketio import join_room, leave_room

LOGGER = logging.getLogger(__name__)
GAME_NAMESPACE = "/game"


def parse_move(move_form):
    from_square = move_form.get('from_square')
    from_square = int(from_square) if from_square is not None else None
    to_square = move_form.get('to_square')
    to_square = int(to_square) if to_square is not None else None
    drop = move_form.get('drop')
    drop = int(drop) if drop is not None else None
    promotion = move_form.get('promotion')
    board_code = move_form.get('board')

    move = chess.Move(from_square=from_square, to_square=to_square,
                      promotion=promotion, drop=drop)
    custom_move = CustomMove(board_code, move)
    return custom_move


def push_move_and_validate(gameid, custom_move):
    game = utils.get_game_from_id(gameid)

    if custom_move.move == chess.Move.null():
        return make_response("Null Move", 400)

    if not game.validate_move(custom_move):
        return make_response("Invalid move", 400)

    game.make_move(custom_move)
    LOGGER.info("pushed move on board " + str(game.id) + "_" + custom_move.board_code + ": " + custom_move.move.uci())

    return make_response("pushed move", 200)


@app.route("/game/<gameid>/move/", methods=["POST"])
def move_a(gameid):
    move = parse_move(request.form.to_dict())
    db.session.commit()
    return push_move_and_validate(gameid, move)


@app.route("/game/view/<gameid>")
def view(gameid):
    LOGGER.info("viewing board")
    game = utils.get_game_from_id(gameid)
    return game.board_a.board.fen() + " and " + game.board_b.board.fen()


@app.route("/game/create", methods=["POST"])
def create_game():
    game = Game()
    db.session.add(game)
    db.session.commit()
    LOGGER.debug("created game with id " + str(game.id))
    return make_response(str(game.id), 201)


@app.route("/game/join/<game_id>", methods=["POST"])
def add_player_to_game(game_id):
    game = utils.get_game_from_id(game_id)
    player_id = request.form['player_id']
    player = utils.get_player_from_id(player_id)
    position = request.form['position']
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
