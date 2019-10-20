from exts import login_manager, db
import datetime
from flask import jsonify



class PickupModel(db.Model):
    __tablename__ = 'pickup'
    id = db.Column(db.Integer, primary_key=True)
    scheduled_date = db.Column(db.DateTime, nullable = False)
    active = db.Column(db.Boolean,default = True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable = False)



    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


