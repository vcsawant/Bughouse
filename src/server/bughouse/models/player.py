from bughouse import db
from marshmallow_sqlalchemy import ModelSchema


class Player(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    elo = db.Column(db.Integer, nullable=False)
    global_wins = db.Column(db.Integer, default=0)
    global_losses = db.Column(db.Integer, default=0)

    def update_result(self, result):
        if result == 0:
            self.elo = self.elo + 10
            self.global_wins = self.global_wins + 1
        elif result == 1:
            self.elo = self.elo - 10
            self.global_losses = self.global_losses + 1


def update_player_result(player_id, result):
    player = Player.query.get(player_id)
    if result == 0:
        player.elo = player.elo + 10
        player.global_wins = player.global_wins + 1
    if result == 1:
        player.elo = player.elo - 10
        player.global_losses = player.global_losses + 1

    db.session.commit()


class PlayerSchema(ModelSchema):
    class Meta:
        model = Player
