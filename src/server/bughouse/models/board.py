import chess
from bughouse import db


class Board:
    id = db.Column(db.Integer, primary_key=True)

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
