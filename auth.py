from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_cred import db, User, TokenBlacklist
import os

# Initialize Flask extensions
login_manager = LoginManager()
jwt = JWTManager()

@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return db.session.query(TokenBlacklist.id).filter_by(jti=jti).scalar() is not None

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200

    return jsonify({"login": "failed"}), 401

@auth_bp.route('/signup', methods=['POST'])
def user_signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    password_hash = generate_password_hash(password)

    new_user = User(email=email, password_hash=password_hash)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({"signup": "success"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"signup": "failed", "reason": str(e)}), 400

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    jti = get_jwt()['jti']
    new_blacklist_token = TokenBlacklist(jti=jti)
    db.session.add(new_blacklist_token)
    db.session.commit()
    return jsonify({"logout": "success"}), 200

def initialize_auth(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp)
    with app.app_context():
        db.create_all()


# from flask import Flask, Blueprint, request, jsonify
# from flask_login import LoginManager, login_user
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
# from werkzeug.security import generate_password_hash, check_password_hash
# from models.user_cred import db, User
# from datetime import datetime, timedelta
# import os

# login_manager = LoginManager()
# jwt = JWTManager()

# # Additional claims loader to include 'iat' claim
# @jwt.additional_claims_loader
# def add_claims_to_access_token(identity):
#     return {'iat': datetime.utcnow()}

# # Token blacklist loader to check 'iat' against 'last_logout'
# @jwt.token_in_blocklist_loader
# def check_if_token_in_blacklist(jwt_header, jwt_payload):
#     email = jwt_payload['sub']
#     user = User.query.get(email)
#     if user.last_logout and jwt_payload['iat'] < user.last_logout.timestamp():
#         return True
#     return False

# # Create a blueprint for authentication routes
# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/login', methods=['POST'])
# def user_login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')
#     user = User.query.filter_by(email=email).first()

#     if user and check_password_hash(user.password_hash, password):
#         access_token = create_access_token(identity=email)
#         return jsonify(access_token=access_token), 200

#     return jsonify({"login": "failed"}), 401

# @auth_bp.route('/signup', methods=['POST'])
# def user_signup():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')
#     password_hash = generate_password_hash(password)

#     new_user = User(email=email, password_hash=password_hash)
#     db.session.add(new_user)
#     try:
#         db.session.commit()
#         return jsonify({"signup": "success"}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"signup": "failed", "reason": str(e)}), 400

# @auth_bp.route('/logout', methods=['POST'])
# @jwt_required()
# def user_logout():
#     email = get_jwt_identity()
#     user = User.query.get(email)
#     user.last_logout = datetime.utcnow()
#     db.session.commit()
#     return jsonify({"logout": "success"}), 200

# def initialize_auth(app):
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)
#     login_manager.init_app(app)
#     jwt.init_app(app)
#     app.register_blueprint(auth_bp)
#     with app.app_context():
#         db.create_all()