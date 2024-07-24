from flask import Flask
from services.geckocoin import coin_gecko
from services.jupiter import coin_jupiter
from services.dexscreener import coin_dex
from services.coin_wallet import coin_wallet
from services.check_app import check_app
from services.top_coins import top_coins
from services.top_coins_data import top_coins_data
from services.holders import holders
from services.coin_details import coin_details
from auth import initialize_auth
# from logout import logout
import os
import psycopg2
from flask_login import login_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from closing_predict import closing_predict

app = Flask(__name__)
app.config.from_object(Config)

url = app.config['SQLALCHEMY_DATABASE_URI']
conn = psycopg2.connect(url)
curr = conn.cursor()

initialize_auth(app)

@app.route("/")
def home():
    return check_app(curr)

@app.route("/geckocoins")
@jwt_required()
# @login_required
def gecko_coins():
    return coin_gecko()

@app.route("/jupitercoin")
@jwt_required()
def jupitercoin():
    return coin_jupiter()

@app.route("/dexscreener_coin/<string:coin_id>")
@jwt_required()
def dexscreener_coin_data(coin_id):
    return coin_dex(coin_id)

@app.route("/wallet/<string:coin_id>")
@jwt_required()
def wallet_data(coin_id):
    return coin_wallet(coin_id)

@app.route("/top_coins_jupiter")
@jwt_required()
def top_coins_jupiter():
    return top_coins()

@app.route("/top_coins_alldata")
@jwt_required()
def top_coins_alldata():
    return top_coins_data()

@app.route("/holders/<string:coin_id>")
@jwt_required()
def coin_holders_data(coin_id):
    return holders(coin_id)

@app.route("/holder_dex_data/<string:coin_id>")
@jwt_required()
def coin_holders_dex_data(coin_id):
    return coin_details(coin_id)

@app.route("/closing_predict/<string:pair_id>")
@jwt_required()
def closing_coin_predict(pair_id):
    return closing_predict(pair_id)

if __name__ == "__main__":
    app.run(debug=True)
