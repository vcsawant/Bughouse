from bughouse.models import Board, Game, GameDatabase
import chess
from flask import request, Response
import logging
from bughouse import app
import string
import random

LOGGER = logging.getLogger(__name__)

gameDB = GameDatabase()


def parse_move(dict):
    from_square = dict.get('from_square')
    from_square = int(from_square) if from_square is not None else None
    to_square = dict.get('to_square')
    to_square = int(to_square) if to_square is not None else None
    drop = dict.get('drop')
    drop = int(drop) if drop is not None else None
    promotion = dict.get('promotion')

    move = chess.Move(from_square=from_square, to_square=to_square,
                      promotion=promotion, drop=drop)
    return move


def push_move_and_validate(move, board):
    move = parse_move(request.form.to_dict())
    if move == chess.Move.null():
        return Response("Null Move", status=400)

    if not board.validate_move(move):
        return Response("Invalid Move", status=400)

    board.move(move)
    LOGGER.info("pushed move on board " + board.identifier + move.uci())

    return Response(status=204)


@app.route("/game/<gameid>/move-a/", methods=["POST"])
def move_a(gameid):
    move = parse_move(request.form.to_dict())
    game = gameDB.lookup(gameid)
    return push_move_and_validate(move, game.board_a)


@app.route("/game/<gameid>/move-b/", methods=["POST"])
def move_b(gameid):
    move = parse_move(request.form.to_dict())
    game = gameDB.lookup(gameid)
    return push_move_and_validate(move, game.board_b)


@app.route("/game/view/<gameid>")
def view(gameid):
    LOGGER.info("viewing board")
    game = gameDB.lookup(gameid)
    return game.board_a.board.fen() + " and " + game.board_b.board.fen()


@app.route("/game/create", methods=["POST"])
def create_game():
    gameid = ''.join(random.choice(string.ascii_letters + string.digits)
                     for i in range(6))
    # TODO: ensure unique id
    game = Game(gameid)
    gameDB.addGame(game)

    return Response(gameid, status=200)
