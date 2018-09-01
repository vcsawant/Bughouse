from bughouse import app, db
from flask import request, render_template, flash, abort, redirect, url_for, make_response, jsonify
from urllib.parse import urljoin, urlparse
from bughouse.models import Player
from flask_login import login_user, logout_user
import bughouse.settings as settings
import logging
import sys
from sqlalchemy.exc import IntegrityError
from bughouse.models import PlayerSchema

LOGGER = logging.getLogger(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return make_response(render_template('login.html'), 200)
    elif request.method == 'POST':
        username = request.form['username']
        player = Player.query.get(username)
        if player == None:
            flash("username does not exist")
        elif not player.verify_password(request.form['password']):
            flash("incorrect username or password")
        else:
            login_user(player)
            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('index'))


@app.route("/logout")
def logout():
    logout_user()


@app.route("/register")
def create_player():
    player_id = request.form['id']
    elo = settings.DEFAULT_ELO
    try:
        elo = request.form['elo']
    except KeyError:
        pass
    except:
        LOGGER.error("Unexpected error:", sys.exc_info()[0])
        return make_response(sys.exc_info()[0], 404)

    player = Player(id=player_id, elo=elo)

    password = request.form['password']
    player.set_password(password)

    try:

        db.session.add(player)
        db.session.commit()
    except IntegrityError:
        return make_response("player already exists", 404)
    except:
        LOGGER.error("Unexpected error:", sys.exc_info()[0])
        return make_response(sys.exc_info()[0], 404)
    return make_response(render_template('login.html'), 201)


# protect against open redirects
# code from below link
# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
