import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

if __name__ == "__main__":
    from bughouse import app
    from bughouse import socketio

    socketio.run(app)
