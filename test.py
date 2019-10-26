from flask import url_for
from app import app
from models.user import UserModel
from models.pickup import PickupModel
from models.address import AddressModel
from exts import db

with app.app_context():
    u = UserModel.query.all()[0]
    print(u.name)
    
