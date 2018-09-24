import chess
from marshmallow_sqlalchemy import ModelSchema
import bughouse.models.player as p
from enum import Enum
from bughouse.models.board import Board
from bughouse.models.player import Player
from bughouse import db
import logging
import datetime
import bughouse.constants as constants

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
    status = db.Column(db.Integer, default=constants.GameStatus.WAITING_FOR_PLAYERS.value, nullable=False)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.board_a = Board()
        self.board_b = Board()
        self.board_a_id = self.board_a.id
        self.board_b_id = self.board_b.id

    def add_player(self, player, position):
        # TODO handle adding a player to position where there is already a player
        if position == constants.PositionCode.WHITE_A.value:
            LOGGER.debug("Adding player to white a: " + player.id)
            self.player_white_a_id = player.id
        elif position == constants.PositionCode.BLACK_A.value:
            LOGGER.debug("Adding player to black a: " + player.id)
            self.player_black_a_id = player.id
        elif position == constants.PositionCode.WHITE_B.value:
            LOGGER.debug("Adding player to white b: " + player.id)
            self.player_white_b_id = player.id
        elif position == constants.PositionCode.BLACK_B.value:
            LOGGER.debug("Adding player to black b: " + player.id)
            self.player_black_b_id = player.id

    def finish_game(self, result_code):

        team_a = []
        team_b = []
        team_a.append(self.player_white_a)
        team_a.append(self.player_black_a)
        team_b.append(self.player_white_b)
        team_b.append(self.player_black_b)

        if result_code == constants.GameStatus.WHITE_WIN:
            winners = team_a
            losers = team_b
        else:
            winners = team_b
            losers = team_a

        self.status = result_code
        for player in winners:
            player.update_result(constants.PlayerResult.WIN)
        for player in losers:
            player.update_result(constants.PlayerResult.LOSS)

        # TODO: handle draw or other result codes in future

    def make_move(self, move):
        if move.board_code == constants.BoardCode.BOARD_A:
            self.board_a.move(move.move)
        else:
            self.board_b.move(move.move)

    def validate_move(self, custom_move):
        if custom_move.board_code == 0:
            return self.board_a.validate_move(custom_move.move)
        else:
            return self.board_b.validate_move(custom_move.move)


class GameSchema(ModelSchema):
    class Meta:
        model = Game


class BughouseMove:
    def __init__(self, board_code, move):
        self.board_code = board_code
        self.move = move
