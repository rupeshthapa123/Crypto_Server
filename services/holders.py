from flask import jsonify
import requests

def holders(coin_id):

    api_url = f'https://api.solana.fm/v1/tokens/{coin_id}/holders'
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