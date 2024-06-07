# from flask import jsonify
# import requests

# def coin_gecko():
#     api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=cad' 
#     # headers = {
#     #     'x_cg_pro_api_key': 'CG-6T5VV59o7CwUsNvkB3UrrQ8N',  
#     #     'Content-Type': 'application/json'
#     # }
#     try:
#         response = requests.get(api_url)
#         data = response.json()
#         return jsonify(data), 200
#     except requests.exceptions.RequestException as e:
#         return jsonify({'error': str(e)}), 500

from flask import jsonify
import requests
import time


def coin_gecko():
    api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=cad'
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(api_url)
            data = response.json()
            return jsonify(data), 200
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= max_retries:
                return jsonify({'error': f"Max retries exceeded: {str(e)}"}), 500
            print(f"Request failed. Retrying... (Attempt {retries}/{max_retries})")
            time.sleep(1)

    return jsonify({'error': 'Unexpected error occurred.'}), 500
