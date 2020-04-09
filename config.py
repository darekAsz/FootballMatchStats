import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DB_URI = os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
