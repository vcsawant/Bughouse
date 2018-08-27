import chess
from marshmallow_sqlalchemy import ModelSchema
import bughouse.models.player as p
from enum import Enum
from bughouse.models.board import Board
from bughouse.models.player import Player
from bughouse import db
import logging
import datetime

LOGGER = logging.getLogger(__name__)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_a_id = db.Column(
        db.Integer, db.ForeignKey('board.id'), nullable=False)
    board_a = db.relationship('Board', foreign_keys=[board_a_id], uselist=False)
    board_b_id = db.Column(
        db.Integer, db.ForeignKey('board.id'), nullable=False)
    board_b = db.relationship('Board', foreign_keys=[board_b_id], uselist=False)

    player_white_a_id = db.Column(db.String(80), db.ForeignKey('player.id'))
    player_white_b_id = db.Column(db.String(80), db.ForeignKey('player.id'))
    player_black_a_id = db.Column(db.String(80), db.ForeignKey('player.id'))
    player_black_b_id = db.Column(db.String(80), db.ForeignKey('player.id'))

    player_white_a = db.relationship('Player', foreign_keys=[player_white_a_id])
    player_white_b = db.relationship('Player', foreign_keys=[player_white_b_id])
    player_black_a = db.relationship('Player', foreign_keys=[player_black_a_id])
    player_black_b = db.relationship('Player', foreign_keys=[player_black_b_id])
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    result = db.Column(db.Integer, nullable=True)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.board_a = Board()
        self.board_b = Board()
        self.board_a_id = self.board_a.id
        self.board_b_id = self.board_b.id

    def add_player(self, player, position):
        if position == 0:
            self.player_white_a = player
            self.player_white_a_id = player.id
        elif position == 1:
            self.player_black_a = player
            self.player_black_a_id = player.id
        elif position == 2:
            self.player_white_b = player
            self.player_white_b_id = player.id
        elif position == 3:
            self.player_black_b = player
            self.player_black_b_id = player.id

    def finish_game(self, result_code):
        winners = [self.player_white_a, self.player_black_a] if result_code == 0 else [
            self.player_white_b, self.player_black_b]
        losers = [self.player_white_a, self.player_black_a] if result_code == 1 else [
            self.player_white_b, self.player_black_b]
        self.result = result_code
        for player in winners:
            p.update_player_result(player.id, Result.WIN)
        for player in losers:
            p.update_player_result(player.id, Result.LOSS)

        # TODO: handle draw or other result codes in future

    def make_move(self, custom_move):
        if custom_move.board_code == 0:
            self.board_a.move(custom_move.move)
        else:
            self.board_b.move(custom_move.move)

    def validate_move(self, custom_move):
        if custom_move.board_code == 0:
            return self.board_a.validate_move(custom_move.move)
        else:
            return self.board_b.validate_move(custom_move.move)


def add_player_and_update(game_id, player, position):
    game = Game.query.get(game_id)
    game.add_player(player, position)


def finish_game_and_update(gameid, result_code):
    game = Game.query.get(gameid)
    game.finish_game(result_code)


def make_move_and_update(game_id, custom_move):
    game = Game.query.get(game_id)
    game.make_move(custom_move)


class GameSchema(ModelSchema):
    class Meta:
        model = Game


class Result(Enum):
    WIN = 0
    LOSS = 1
    DRAW = 2
    IN_PROGRESS = None


class CustomMove:
    def __init__(self, board_code, move):
        self.board_code = board_code
        self.move = move
