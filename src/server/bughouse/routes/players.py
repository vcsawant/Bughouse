from bughouse import app, db
import logging
from bughouse.models import Player
from bughouse.models.player import PlayerSchema
from flask import request, make_response, jsonify
from flask_login import login_required, current_user
import bughouse.utils as utils

LOGGER = logging.getLogger(__name__)


@app.route("/player/view/<player_id>")
def view_player(player_id):
    player = utils.get_player_from_id(player_id)
    if player is None:
        return make_response("No such player", 400)
    return make_response(jsonify(player_schema.dump(player).data), 200)


@app.route("/player/view")
@login_required
def view_all_players():
    players = Player.query.all()
    return jsonify(PlayerSchema(many=True).dump(players).data)


@app.context_processor
def inject_current_user():
    return dict(user=PlayerSchema().dump(current_user))
