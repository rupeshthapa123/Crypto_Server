from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user_cred'
    email = db.Column(db.String(150), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    last_logout = db.Column(db.DateTime, nullable=True)

class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)