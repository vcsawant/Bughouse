from bughouse import db


class Player(db.Model):

    id = db.Column(db.String(80), primary_key=True)
    elo = db.Column(db.Integer, nullable=False)

    def __init__(self, identifier):
        self.identifier = identifier
        self.elo = 1000
