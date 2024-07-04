from flask import jsonify
import requests

def extract_keys(data, keys_to_extract):
    extracted_data = {}
    try:
        for key in keys_to_extract:
            if key in data:
                extracted_data[key] = data[key]
            elif key == "liquidity":
                extracted_data[key] = data["dex_data"]["liquidity"]
            elif key == "volume":
                extracted_data[key] = data["dex_data"]["volume"]

        return extracted_data
    except Exception as e:
        print(e)
        return extracted_data

def top_coins_data():
    api_url_jupiter = 'https://stats.jup.ag/coingecko/tickers' 
    api_url_dex = 'https://api.dexscreener.com/latest/dex/tokens/'
    keys_to_extract = ["base_currency", "base_volume", "liquidity", "volume", "high", "last_price", "low"]
    final_res = []

    try:
        response = requests.get(api_url_jupiter)
        data = response.json()
        result = []
        i = 0

        while i<=19:
            result.append(data[i])
            i+=1

        for i in range(len(result)):
            try:
                response = requests.get(f"{api_url_dex}{result[i]["base_address"]}")
                data = response.json()
                data = data["pairs"][0]
                result[i]["dex_data"] = data
            except Exception as e:
                result[i]["dex_data"] = "null"

        for dics in result:
            final_res.append(extract_keys(dics, keys_to_extract))
    
        return jsonify(final_res), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500