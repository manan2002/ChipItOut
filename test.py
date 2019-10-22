from flask import url_for
from app import app
from models.user import UserModel
from models.pickup import PickupModel
from models.address import AddressModel
from exts import db

with app.app_context():
    #u = UserModel.query.all()[0]
    #addr = AddressModel(_address = 'blah blah blah', zone = 'sw', user = u)
    #addr.save()
    #print(len(u.pickups))
    #print(url_for('dashboard.address', next = url_for('dashboard.settings')))
    #print(u.points)
    addr = AddressModel.query.all()[0]
    print(addr._address, addr.zone)
