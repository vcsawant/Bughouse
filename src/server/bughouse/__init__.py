from flask import Flask, render_template
import bughouse.settings as settings
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__, static_folder="../../static/dist",
            template_folder="../../static")
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI
app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO
app.config['DEBUG'] = settings.DEBUG
app.config['SECRET_KEY'] = settings.SECRET_KEY

toolbar = DebugToolbarExtension(app)

socketio = SocketIO(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello")
def hello():
    return "Hello World"


import bughouse.routes
import bughouse.connection
