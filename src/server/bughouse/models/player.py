from bughouse import db
from marshmallow_sqlalchemy import ModelSchema
import bughouse.constants as constants
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from bughouse import login


class Player(db.Model, UserMixin):
    id = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(80), nullable=False)
    elo = db.Column(db.Integer, default=1200, nullable=False)
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

    def set_password(self, password_text):
        self.password_hash = generate_password_hash(password_text)

    def verify_password(self, password_text):
        return check_password_hash(self.password_hash, password_text)


class PlayerSchema(ModelSchema):
    class Meta:
        model = Player


@login.user_loader
def user_loader(user_id):
    return Player.query.get(user_id)
