import chess
from bughouse import db
from marshmallow_sqlalchemy import ModelSchema


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placeable_white = db.Column(db.String(10), default="p0k0b0r0q0", nullable=False)
    placeable_black = db.Column(db.String(10), default="p0k0b0r0q0", nullable=False)
    board_fen = db.Column(db.String(80), default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                          nullable=False)
    board = chess.Board()

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)

    def validate_move(self, move):
        # TODO: complete definition
        return True

    def move(self, move):
        self.board.push(move)
        self.board_fen = self.board.fen()


class BoardSchema(ModelSchema):
    class Meta:
        model = Board
