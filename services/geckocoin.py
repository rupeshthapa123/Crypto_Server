from flask import jsonify
import requests
import time
from helpers import fetch_data_from_api
from constants import *

def coin_gecko():
    api_url = gecko_coin
    data = fetch_data_from_api(api_url)
    data = data.get_json()
    if "payload" not in data:
        return jsonify(data), 500
    ### need to write logic here
    return jsonify(data)



