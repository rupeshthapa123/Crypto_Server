from flask import jsonify
import requests

def auth(password):
    try:
        if password == "password":
            data = {"success": True, "access":"granted"}
        else:
            data = {"success": True, "access":"denied"}

        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

