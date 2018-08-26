import chess
from bughouse.models.board import Board
from bughouse.models.player import Player
from bughouse import db
from flask import request, Response
import logging
import datetime


LOGGER = logging.getLogger(__name__)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_a_id = db.Column(
        db.Integer,  db.ForeignKey('board.id'), nullable=False)
    board_b_id = db.Column(
        db.Integer, db.ForeignKey('board.id'), nullable=False)
    player_white_a_id = db.Column(db.String(80), db.ForeignKey('player.id'))
    player_white_b_id = db.Column(db.String(80), db.ForeignKey('player.id'))
    player_black_a_id = db.Column(db.String(80), db.ForeignKey('player.id'))
    player_black_b_id = db.Column(db.String(80), db.ForeignKey('player.id'))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    result = db.Column(db.Integer)

    def __init__(self, identifier):
        self.id = identifier
        self.player_white_a = None
        self.player_white_b = None
        self.player_black_a = None
        self.player_black_b = None
        self.spectator_list = []
        self.result = None

    def add_player(self, player, position):
        if position == 0:
            self.player_white_a = player
        elif position == 1:
            self.player_black_a = player
        elif position == 2:
            self.player_white_b = player
        elif position == 3:
            self.player_black_b = player
        else:
            self.spectator_list.append(player)

    def finish_game(self, result_code):
        winners = [self.player_white_a, self.player_black_a] if result_code == 0 else [
            self.player_white_b, self.player_black_b]
        # TODO: manage elo updates and database updates

# temporary solution only


class GameDatabase:
    def __init__(self):
        self.games = {}

    def lookup(self, gameid):
        if gameid in self.games:
            return self.games[gameid]
        raise ValueError("gameid not found")

    def addGame(self, game):
        self.games[game.gameid] = game
