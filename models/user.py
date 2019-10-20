from exts import login_manager, db
from datetime import datetime
from flask import jsonify
from flask_login import UserMixin


class UserModel(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(300), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable=False)
    pickups = db.relationship('PickupModel', backref='user')
    can_schedule = db.Column(db.Boolean, default = True)
    points = db.Column(db.Integer, default = 0)
    def __str__(self):
        return f'{self.email}'

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


@login_manager.user_loader
def loadUser(user_id):
    return UserModel.query.get(user_id)
