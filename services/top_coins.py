from flask import jsonify
import requests
from constants import *

def top_coins():
    api_url = jupiter_top_coins 
    try:
        response = requests.get(api_url)
        data = response.json()
        res = []
        i = 0
        while i<=99:
            res.append(data[i])
            i+=1
        return jsonify(res), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500