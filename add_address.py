from flask import url_for
from app import app
from models.user import UserModel
from models.pickup import PickupModel
from models.address import AddressModel
from exts import db
from datetime import datetime

with app.app_context():
    u = UserModel.query.all()[0]
    
    home_addr = AddressModel.query.filter_by(label='Home').first()
    office_addr = AddressModel.query.filter_by(label='Office').first()

    dt = datetime(2019,10,3)
    p = PickupModel(
        scheduled_date = dt,
        user = u,
        address = home_addr,
        active = False,   
        description = 'A fridge',
        completed = True
    )
    db.session.add(p)
    
    dt = datetime(2019, 10, 10)
    p = PickupModel(
        scheduled_date=dt,
        user=u,
        address=office_addr,
        active=False,
        description='An old phone',
        completed=True
    )
    db.session.add(p)

    dt = datetime(2019, 10, 22)
    p = PickupModel(
        scheduled_date=dt,
        user=u,
        address=home_addr,
        active=False,
        description='10 AA batteries',
        completed=True
    )
    db.session.add(p)
    db.session.commit()
    


    

    
