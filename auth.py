from flask import Blueprint, request
from flask_login import LoginManager, UserMixin, login_user
import json
import os
from VARS import USERS

login_manager = LoginManager()

# Predefined users
predefined_users = USERS

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

@login_manager.user_loader
def load_user(username):
    if username in predefined_users:
        return User(username)
    return None

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_hash = predefined_users.get(username)
        if user_hash and predefined_users[username] == password:
            user = User(username)
            login_user(user)
            return {"login": "success"}
    return {"Need": "login"}

def initialize_auth(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.user_login'
    app.register_blueprint(auth_bp)
