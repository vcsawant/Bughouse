from bughouse import app, db
from flask import request, render_template, flash, abort, redirect, url_for, make_response
from urllib.parse import urljoin, urlparse
from bughouse.models import Player
from flask_login import login_user, logout_user
import bughouse.settings as settings
import logging
import sys
from sqlalchemy.exc import IntegrityError

LOGGER = logging.getLogger(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return make_response(render_template('login.html'), 200)
    elif request.method == 'POST':
        request_json = request.get_json(force=True, silent=True)
        username = request_json.get('username', None)
        password = request_json.get('password', None)
        remember = request.form.get('remember_me', False)

        if username == None or password == None:
            return make_response("error logging in", 400)

        player = Player.query.get(username)

        if player == None:
            flash("username does not exist")
        elif not player.verify_password(password):
            flash("incorrect username or password")
        else:
            login_user(player, remember=remember)
            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('index'))
    else:
        make_response("unrecognized http code", 400)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def create_player():
    if request.method == 'POST':
        LOGGER.info(str(request.json))
        request_json = request.get_json(force=True, silent=True)
        player_id = request_json.get('username', None)

        LOGGER.info("player_id from request: " + str(player_id))
        elo = request_json.get('elo', settings.DEFAULT_ELO)

        password = request_json.get('password', None)

        if player_id == None or password == None:
            return make_response("player registration error", 400)

        player = Player(id=player_id, elo=elo)
        player.set_password(password)

        try:

            db.session.add(player)
            db.session.commit()
        except IntegrityError:
            return make_response("player already exists", 400)
        except:
            LOGGER.error("Unexpected error:", sys.exc_info()[0])
            return make_response(sys.exc_info()[0], 400)

        return make_response("registered player", 200)
    return make_response(render_template('register.html'), 201)


# protect against open redirects
# code from below link
# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
