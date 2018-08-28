from bughouse import db
from marshmallow_sqlalchemy import ModelSchema
import bughouse.constants as constants


class Player(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    elo = db.Column(db.Integer, nullable=False)
    global_wins = db.Column(db.Integer, default=0)
    global_losses = db.Column(db.Integer, default=0)

    def update_result(self, result):
        # TODO: handle other result codes
        if result == constants.PlayerResult.WIN:
            self.elo = self.elo + 10
            self.global_wins = self.global_wins + 1
        elif result == constants.PlayerResult.LOSS:
            self.elo = self.elo - 10
            self.global_losses = self.global_losses + 1


class PlayerSchema(ModelSchema):
    class Meta:
        model = Player
