import os

DB_URI = os.environ.get("BUGHOUSE_DB_URI", "sqlite:///bughouse.development")
