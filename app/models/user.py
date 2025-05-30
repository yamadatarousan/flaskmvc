from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Taskモデルとの関連付け（カスケード削除を設定）
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Profileモデルとの関連付け（カスケード削除を設定）
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        """パスワードをハッシュ化して設定"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """パスワードの検証"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'