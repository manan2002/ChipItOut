from flask import Flask, jsonify, render_template
import click
from exts import db, login_manager
from models.user import UserModel
from models.pickup import PickupModel
from views.auth import auth
from views.dashboard import dashboard
from werkzeug.security import generate_password_hash

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
