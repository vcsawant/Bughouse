from bughouse import app, db
import logging
from bughouse.models import Player
from bughouse.models.player import PlayerSchema
from flask import request, make_response, jsonify
import sys
import bughouse.utils as utils
from sqlalchemy.exc import IntegrityError
import bughouse.settings as settings

LOGGER = logging.getLogger(__name__)


@app.route("/player/view/<player_id>")
def view_player(player_id):
    player = utils.get_player_from_id(player_id)
    if player is None:
        return make_response("No such player", 404)
    return jsonify(PlayerSchema().dump(player).data)


@app.route("/player/view")
def view_all_players():
    players = Player.query.all()
    return jsonify(PlayerSchema(many=True).dump(players).data)
