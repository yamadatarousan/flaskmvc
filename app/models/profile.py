from app import db
from datetime import datetime

class Profile(db.Model):
    __tablename__ = 'profiles'  # 複数形に統一
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)  # usersテーブルを参照
    birth_date = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Userモデルとの関連付け
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    def __repr__(self):
        return f'<Profile {self.id}>' 