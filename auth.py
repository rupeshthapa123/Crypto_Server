from flask import Blueprint, request, jsonify
from flask_login import LoginManager, UserMixin, login_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
import os
import psycopg2
import datetime

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, email):
        self.id = email
        self.email = email

@login_manager.user_loader
def load_user(email):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    curr = conn.cursor()
    curr.execute("SELECT email FROM user_cred WHERE email = %s", (email,))
    user = curr.fetchone()
    conn.close()
    if user:
        return User(user[0])
    return None

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    curr = conn.cursor()
    curr.execute("SELECT 1 FROM token_blacklist WHERE jti = %s", (jti,))
    result = curr.fetchone()
    conn.close()
    return result is not None

@auth_bp.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    curr = conn.cursor()
    curr.execute("SELECT password_hash FROM user_cred WHERE email = %s", (email,))
    user = curr.fetchone()
    conn.close()

    if user and check_password_hash(user[0], password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200

    return jsonify({"login": "failed"}), 401

@auth_bp.route('/signup', methods=['POST'])
def user_signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    password_hash = generate_password_hash(password)

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    curr = conn.cursor()
    try:
        curr.execute("INSERT INTO user_cred (email, password_hash) VALUES (%s, %s)", (email, password_hash))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"signup": "failed", "reason": str(e)}), 400
    finally:
        conn.close()

    return jsonify({"signup": "success"}), 201

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    jti = get_jwt()['jti']
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    curr = conn.cursor()
    curr.execute("INSERT INTO token_blacklist (jti) VALUES (%s)", (jti,))
    conn.commit()
    conn.close()
    return jsonify({"logout": "success"}), 200

def initialize_auth(app):
    login_manager.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp)

    