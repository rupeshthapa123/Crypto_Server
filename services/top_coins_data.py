from flask import jsonify
import requests

def top_coins_data():
    api_url_jupiter = 'https://stats.jup.ag/coingecko/tickers' 
    api_url_dex = 'https://api.dexscreener.com/latest/dex/tokens/'
    try:
        response = requests.get(api_url_jupiter)
        data = response.json()
        result = []
        i = 0

        while i<=49:
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
        
        ### need to work on result
    
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500