from flask import jsonify
import requests
from constants import *

def coin_jupiter():
    api_url = jupiter_coins
    # headers = {
    #     'x_cg_pro_api_key': 'CG-6T5VV59o7CwUsNvkB3UrrQ8N',  
    #     'Content-Type': 'application/json'
    # }
    try:
        response = requests.get(api_url)
        data = response.json()
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

