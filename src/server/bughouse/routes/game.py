from bughouse.models import Game, Player, Board, GameSchema
from bughouse.models.game import CustomMove
import chess
from flask import request, make_response, jsonify
import logging
from bughouse import app, db

LOGGER = logging.getLogger(__name__)


def parse_move(move_dict):
    from_square = move_dict.get('from_square')
    from_square = int(from_square) if from_square is not None else None
    to_square = move_dict.get('to_square')
    to_square = int(to_square) if to_square is not None else None
    drop = move_dict.get('drop')
    drop = int(drop) if drop is not None else None
    promotion = move_dict.get('promotion')
    board_code = move_dict.get('board')

    move = chess.Move(from_square=from_square, to_square=to_square,
                      promotion=promotion, drop=drop)
    custom_move = CustomMove(board_code, move)
    return custom_move


def get_game_from_id(gameid):
    return Game.query.get(gameid)


def push_move_and_validate(gameid, custom_move):
    game = get_game_from_id(gameid)

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
    game = get_game_from_id(gameid)
    return game.board_a.board.fen() + " and " + game.board_b.board.fen()


@app.route("/game/create", methods=["POST"])
def create_game():
    game = Game()
    db.session.add(game)
    db.session.commit()
    LOGGER.debug("created game with id " + str(game.id))
    return make_response(str(game.id))


@app.route("/game/view")
def view_all_games():
    LOGGER.info("viewing all games")
    games = Game.query.all()
    return jsonify(GameSchema(many=True).dump(games).data)


#################################################
#   DEBUG TOOLS                                 #
#################################################

@app.route("/debug/drop", methods=["POST"])
def drop_db():
    db.drop_all()


@app.route("/debug/create", methods=["POST"])
def create_db():
    db.create_all()
