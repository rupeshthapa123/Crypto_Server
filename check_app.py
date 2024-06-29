from flask import jsonify
import requests


def check_app(curr):
    try:
        curr.execute('SELECT version();')
        db_version = curr.fetchone()
        data = {"success": True, "payload": "Server running...", "db_version": db_version}
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500