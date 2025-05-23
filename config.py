import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLiteからMySQLに戻す
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/flaskmvc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-key-for-testing'
    DEBUG = True