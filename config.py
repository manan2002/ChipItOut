import os


class Config(object):

    #Base configs
    SECRET_KEY = os.urandom(30)

    #Flask-SQLAlchemy configs.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
