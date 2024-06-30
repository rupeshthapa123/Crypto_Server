from flask import jsonify
import requests
import time
from services.functions import fetch_data_from_api

def coin_gecko():
    api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=cad'
    data = fetch_data_from_api(api_url)
    data = data.get_json()
    if "payload" not in data:
        return jsonify(data), 500
    ### need to write logic here
    return jsonify(data)



