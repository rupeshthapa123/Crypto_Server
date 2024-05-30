from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/")
def Home():
    try:
        data = {"success": True, "payload": "/* Application-specific data would go here. */"}
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@app.route("/password/<string:password>")
def user_password_auth(password):
    try:
        if password == "password":
            data = {"success": True, "access":"granted"}
        else:
            data = {"success": True, "access":"denied"}

        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@app.route("/geckocoins")
def gecko_coins():
    api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=cad' 
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


@app.route("/jupitercoin")
def jupitercoin():

    api_url = 'https://token.jup.ag/strict' 
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


@app.route("/dexscreener_coin/<string:coin_id>")
def dexscreener_coin_data(coin_id):

    api_url = f'https://api.dexscreener.com/latest/dex/tokens/{coin_id}'
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


if __name__ ==  "__main__":
    app.run(debug=True)


