from flask import Flask, jsonify, render_template
import click
from exts import db, login_manager
from models.user import UserModel
from models.pickup import PickupModel
from models.address import AddressModel
from models.quote import QuoteModel
from views.auth import auth
from views.dashboard import dashboard
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy.sql.expression import func

app = Flask(__name__)

app.config.from_object('config.Config')

login_manager.init_app(app)
db.init_app(app)


"""
Registering blueprints.
"""
app.register_blueprint(auth)
app.register_blueprint(dashboard)

@app.before_first_request
def create_db():
    db.create_all()

"""
General routes.
"""
@app.route('/')
def index():
    return render_template('general/index.html')

@app.route('/quote')
def quote():
    q = QuoteModel.query.order_by(func.random()).first()
    return jsonify({
        'quote' : q.text
    })

"""
Custom CLI Commands below.
"""
@app.cli.command('delete-all-users')
def deleteAllUsers():
    users = UserModel.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    print('All users deleted.')

@app.cli.command('create-user')
@click.option('--count', default = 1)
def createUser(count=1):
    count = int(count)
    for _ in range(count):
        name = input('Enter name: ').strip()
        email = input('Enter email: ').strip()
        pw = generate_password_hash(input('Enter password: ').strip())
        u = UserModel(email=email, name=name, password=pw)
        u = u.save()
        print(f'User - {u} created.')


@app.cli.command('list-users')
@click.option('--count', default = -1)
def listUsers(count):
    count = int(count)
    q = UserModel.query.order_by(UserModel.id)
    if count == -1:
        users = q.all()
    else:
        users = q.limit(count)
    for u in users:
        print(u)


@app.cli.command('add-data')
def add_data():
    name, email, pw = 'Man', 'demo@hotmail.com', 'demopass'
    pw_hash = generate_password_hash(pw)
    u = UserModel(
        email=email, 
        name=name, 
        password=pw_hash)
    u.save()
    label, addr, zone = 'Home', 'J-35, Rajouri Garden', 'n'
    address = AddressModel(
        label=label,
        _address=addr,
        zone=zone,
        user=u,default=True)
    address.save()
    label, addr, zone = 'Office', 'F-132, Rajouri Garden', 'n'
    address = AddressModel(
        label=label,
        _address=addr,
        zone=zone,
        user=u)
    address.save()
    
    home_addr = AddressModel.query.filter_by(label='Home').first()
    office_addr = AddressModel.query.filter_by(label='Office').first()

    dt = datetime(2019, 10, 3)
    p = PickupModel(
        scheduled_date=dt,
        user=u,
        address=home_addr,
        active=False,
        description='A fridge',
        completed=True
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

@app.cli.command('restart-db')
def restartDB():
    db.drop_all()
    db.create_all()
    print('DB restarted.')


@app.cli.command('drop-db')
def restartDB():
    db.drop_all()
    print('DB dropped.')


@app.cli.command('create-db')
def restartDB():
    db.create_all()
    print('DB created.')



if __name__ == '__main__':
    app.run(debug=True)
