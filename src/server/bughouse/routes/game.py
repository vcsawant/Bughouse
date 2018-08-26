import chess
from chess import Move
from bughouse import app
from flask import request, Response
import logging

LOGGER = logging.getLogger(__name__)

board_a = chess.Board()
board_b = chess.Board()

placeable_white_a = []
placeable_white_b = []
placeable_black_a = []
placeable_black_b = []


def dict_to_move(dict):
    from_square = dict.get('from_square', None)
    to_square = dict.get('to_square', None)
    promotion = dict.get('promotion', None)
    drop = dict.get('drop', None)

    move = Move(from_square=int(from_square), to_square=int(to_square),
                promotion=promotion, drop=drop)
    return move


@app.route("/board/move-a/", methods=["POST"])
def move_a():
    move = dict_to_move(request.form.to_dict())
    if move != Move.null():
        board_a.push(move)
        LOGGER.info("pushed move")
        LOGGER.debug("move on board A: " + move.uci())

        return Response(status=204)

    return Response("Move unable to be parsed", status=400)


@app.route("/board/move-b/", methods=["POST"])
def move_b():
    move = dict_to_move(request.form.to_dict())
    if move != Move.null():
        board_b.push(move)
        LOGGER.info("pushed move")
        LOGGER.debug("move on board B: " + move.uci())

        return Response(status=204)

    return Response("Move unable to be parsed", status=400)


@app.route("/board/view")
def view():
    LOGGER.info("viewing board")
    return board_a.fen() + " and " + board_b.fen()
