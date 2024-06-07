from flask import jsonify
from flask_login import logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests


def logout():
    try:
        logout_user()
        return {"logout":"success"}, 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


