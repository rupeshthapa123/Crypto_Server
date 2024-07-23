from flask import jsonify
import requests
import concurrent.futures
from constants import *

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

def fetch_dex_data(base_address):
    api_url_dex = dex_single_coin
    try:
        response = requests.get(f'{api_url_dex}{base_address}')
        data = response.json()
        return data["pairs"][0]
    except Exception as e:
        return None

def top_coins_data():
    api_url_jupiter = jupiter_top_coins
    keys_to_extract = ["base_currency", "base_address", "base_volume", "liquidity", "volume", "high", "last_price", "low"]
    final_res = []

    try:
        response = requests.get(api_url_jupiter)
        data = response.json()
        result = data[:20]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            dex_data_futures = {executor.submit(fetch_dex_data, coin["base_address"]): coin for coin in result}

            for future in concurrent.futures.as_completed(dex_data_futures):
                coin = dex_data_futures[future]
                try:
                    dex_data = future.result()
                    if dex_data:
                        coin["dex_data"] = dex_data
                    else:
                        coin["dex_data"] = "null"
                except Exception as e:
                    coin["dex_data"] = "null"

        final_res = [extract_keys(coin, keys_to_extract) for coin in result]

        return jsonify(final_res), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# from flask import jsonify
# import requests

# def extract_keys(data, keys_to_extract):
#     extracted_data = {}
#     try:
#         for key in keys_to_extract:
#             if key in data:
#                 extracted_data[key] = data[key]
#             elif key == "liquidity":
#                 extracted_data[key] = data["dex_data"]["liquidity"]
#             elif key == "volume":
#                 extracted_data[key] = data["dex_data"]["volume"]

#         return extracted_data
#     except Exception as e:
#         print(e)
#         return extracted_data

# def top_coins_data():
#     api_url_jupiter = 'https://stats.jup.ag/coingecko/tickers' 
#     api_url_dex = 'https://api.dexscreener.com/latest/dex/tokens/'
#     keys_to_extract = ["base_currency", "base_volume", "liquidity", "volume", "high", "last_price", "low"]
#     final_res = []

#     try:
#         response = requests.get(api_url_jupiter)
#         data = response.json()
#         result = []
#         i = 0

#         while i<=99:
#             result.append(data[i])
#             i+=1

#         for i in range(len(result)):
#             try:
#                 response = requests.get(f'{api_url_dex}{result[i]["base_address"]}')
#                 data = response.json()
#                 data = data["pairs"][0]
#                 result[i]["dex_data"] = data
#             except Exception as e:
#                 result[i]["dex_data"] = "null"

#         for dics in result:
#             final_res.append(extract_keys(dics, keys_to_extract))
    
#         return jsonify(final_res), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500