from flask import Flask, jsonify, request
from authentication import auth
from geckocoin import coin_gecko
from jupiter import coin_jupiter
from dexscreener import coin_dex
from coin_wallet import coin_wallet
from check_app import check_app
import requests
import os
import psycopg2


app = Flask(__name__)

url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(url)
curr = conn.cursor()


@app.route("/")
def home():
    return check_app(curr)


# for authentication
@app.route("/password/<string:password>")
def user_password_auth(password):
    return auth(password)


# get top 100 crypto data
@app.route("/geckocoins")
def gecko_coins():
    return coin_gecko()


# get top 100 coin in solona
@app.route("/jupitercoin")
def jupitercoin():
    return coin_jupiter()


# get data for sigle coin
@app.route("/dexscreener_coin/<string:coin_id>")
def dexscreener_coin_data(coin_id):
    return coin_dex(coin_id)


# get the wallet data 
@app.route("/wallet/<string:coin_id>")
def wallet_data(coin_id):
    return coin_wallet(coin_id)

