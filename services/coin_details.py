from flask import jsonify
import requests
from constants import *

def coin_details(coin_id):
    dex_coin_url = dex_coin_data.format(coin_id=coin_id)
    holders_url = sol_holder_coin.format(coin_id=coin_id)

    dex_arr = ["baseToken","quoteToken","priceUsd","txns","volume","priceChange","liquidity","fdv"]
    holder_arr = ["owner","state","uiAmount"]

    try:
        dex_resp = requests.get(dex_coin_url)
        holders_resp = requests.get(holders_url)
        
        dex_data_resp = dex_resp.json()
        holders_data_resp = holders_resp.json()

        dex_data_resp = dex_data_resp["pairs"][0]
        dex_data = {key: dex_data_resp[key] for key in dex_arr}

        holders_data_resp = holders_data_resp["tokenAccounts"]
        holders_data = []

        print(holders_data_resp)

        for i in holders_data_resp:
            holders_data.append({key: i['info'][key] if key in i['info'] else i['info']['tokenAmount'][key] for key in holder_arr})
        
        print(holders_data)

        data = {"dex_data":dex_data, "holders_data":holders_data}

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
