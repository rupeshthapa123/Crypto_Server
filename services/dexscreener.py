from flask import jsonify
import requests
from constants import *

def coin_dex(coin_id):

    api_url = dex_coin_data.format(coin_id=coin_id)
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