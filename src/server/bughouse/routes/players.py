from bughouse import app, db
import logging
from bughouse.models import Player
from bughouse.models.player import PlayerSchema
from flask import request, make_response, jsonify
import sys
import bughouse.utils as utils
from sqlalchemy.exc import IntegrityError

LOGGER = logging.getLogger(__name__)


@app.route("/player/create", methods=["POST"])
def create_player():
    player_id = request.form['id']
    elo = 1200
    try:
        elo = request.form['elo']
    except KeyError:
        pass
    except:
        LOGGER.error("Unexpected error:", sys.exc_info()[0])
        return make_response(sys.exc_info()[0], 404)

    player = Player(id=player_id, elo=elo)

    try:

        db.session.add(player)
        db.session.commit()
    except IntegrityError:
        return make_response("player already exists", 404)
    except:
        LOGGER.error("Unexpected error:", sys.exc_info()[0])
        return make_response(sys.exc_info()[0], 404)
    return make_response(jsonify(PlayerSchema().dump(player).data), 201)


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
