from flask import Flask, jsonify
from exts import db, login_manager
from models.user import UserModel
from views.auth import auth

app = Flask(__name__)

app.config.from_object('config.Config')

login_manager.init_app(app)
db.init_app(app)

app.register_blueprint(auth)

@app.before_first_request
def create_db():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
