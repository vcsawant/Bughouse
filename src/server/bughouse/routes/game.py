import chess
from chess import Move
from bughouse import app
from flask import request, Response
import logging

LOGGER = logging.getLogger(__name__)


class Board:
    def __init__(self, identifier):
        self.board = chess.Board()
        self.identifier = identifier
        self.placeable_white = [0, 0, 0, 0, 0]
        self.placeable_black = [0, 0, 0, 0, 0]

    def validate_move(self, move):
        # TODO: complete definition
        return True

    def move(self, move):
        self.board.push(move)


board_a = Board("A")
board_b = Board("B")


def parse_move(dict):
    from_square = dict.get('from_square')
    from_square = int(from_square) if from_square is not None else None
    to_square = dict.get('to_square')
    to_square = int(to_square) if to_square is not None else None
    drop = dict.get('drop')
    drop = int(drop) if drop is not None else None
    promotion = dict.get('promotion')

    move = Move(from_square=from_square, to_square=to_square,
                promotion=promotion, drop=drop)
    return move


def push_move_and_validate(move, board):
    move = parse_move(request.form.to_dict())
    if move == Move.null():
        return Response("Null Move", status=400)

    if not board.validate_move(move):
        return Response("Invalid Move", status=400)

    board.move(move)
    LOGGER.info("pushed move on board " + board.identifier + move.uci())

    return Response(status=204)


@app.route("/game/move-a/", methods=["POST"])
def move_a():
    move = parse_move(request.form.to_dict())
    return push_move_and_validate(move, board_a)


@app.route("/game/move-b/", methods=["POST"])
def move_b():
    move = parse_move(request.form.to_dict())
    return push_move_and_validate(move, board_b)


@app.route("/game/view")
def view():
    LOGGER.info("viewing board")
    return board_a.board.fen() + " and " + board_b.board.fen()
