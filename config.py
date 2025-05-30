import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLiteからMySQLに戻す
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/flaskmvc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-key-for-testing'
    DEBUG = True
    
    # ログ設定
    LOG_DIR = os.path.join(basedir, 'storage', 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'flask.log')
    LOG_LEVEL = 'INFO'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5