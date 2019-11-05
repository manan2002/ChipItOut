from exts import login_manager, db
import datetime
from flask import jsonify


class AddressModel(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, nullable = False)
    _address = db.Column(db.String(500), nullable = False)
    zone = db.Column(db.String(100), nullable = False)
    default = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pickups = db.relationship('PickupModel', backref='address')
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
