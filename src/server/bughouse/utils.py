from bughouse.models import Player, Game
from bughouse.models.player import PlayerSchema
from bughouse.models.game import GameSchema


def get_player_from_id(player_id):
    player = Player.query.get(player_id)
    if player is None:
        # todo: handle player not exists in db
        pass
    return player


def get_game_from_id(game_id):
    game = Game.query.get(game_id)
    if game is None:
        # todo: handle game not exists in db
        pass
    return game


game_schema = GameSchema()
games_schema = GameSchema(many=True)
player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
