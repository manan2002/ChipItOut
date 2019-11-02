from flask import url_for
from app import app
from models.user import UserModel
from models.pickup import PickupModel
from models.address import AddressModel
from exts import db
from datetime import datetime

with app.app_context():
    u = UserModel.query.all()[0]
    
    
    dt = datetime(2019, 10, 20)
    p = PickupModel(scheduled_date = dt, description = "A fridge", address = addr, active = False, completed = True, user = u)
    
    dt = datetime(2019, 10, 20)
    p = PickupModel(scheduled_date=dt, description="A fridge",
                    address=addr, active=False, completed=True, user=u)
    db.session.commit()
    


    

    
