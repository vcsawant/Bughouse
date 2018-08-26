from flask import Flask, render_template
import bughouse.settings as settings
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__, static_folder="../../static/dist",
            template_folder="../../static")
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI


db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello")
def hello():
    return "Hello World"


import bughouse.routes
