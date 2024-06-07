from flask import Flask
from geckocoin import coin_gecko
from jupiter import coin_jupiter
from dexscreener import coin_dex
from coin_wallet import coin_wallet
from check_app import check_app
from auth import initialize_auth
from logout import logout
import os
import psycopg2
from flask_login import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(url)
curr = conn.cursor()

initialize_auth(app)

@app.route("/")
def home():
    return check_app(curr)

@app.route('/logout')
@login_required
def user_logout():
    return logout()

@app.route("/geckocoins")
@login_required
def gecko_coins():
    return coin_gecko()

@app.route("/jupitercoin")
@login_required
def jupitercoin():
    return coin_jupiter()

@app.route("/dexscreener_coin/<string:coin_id>")
@login_required
def dexscreener_coin_data(coin_id):
    return coin_dex(coin_id)

@app.route("/wallet/<string:coin_id>")
@login_required
def wallet_data(coin_id):
    return coin_wallet(coin_id)

if __name__ == "__main__":
    app.run(debug=True)