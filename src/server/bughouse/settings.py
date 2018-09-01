import os

# TODO: just fix all of this
DB_URI = os.environ.get("BUGHOUSE_DB_URI", "sqlite:////Users/virensawant/Documents/Bughouse/bughouse.development.db")
SQLALCHEMY_ECHO = True
DEBUG = os.environ.get("BUGHOUSE_DEBUG", True)
SECRET_KEY = os.environ.get("BUGHOUSE_SECRET_KEY", "9/?^*sh*.")
DEFAULT_ELO = 1200
