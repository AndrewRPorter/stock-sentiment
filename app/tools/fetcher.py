import datetime
import os

import requests
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_NAME = "../config.yml"
CONFIG_DATA = yaml.safe_load(open(os.path.join(BASE_DIR, CONFIG_NAME)))

api_key = CONFIG_DATA["config"]["API_KEY"]


def get_all_news(ticker):
    """Returns latest ticker specific news from IEX Group API"""
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    sort = "popularity"
    url = f"https://newsapi.org/v2/everything?q={ticker}&from={date}&sortBy={sort}&apiKey={api_key}"
    data = requests.get(url).json()
    return data


def invalid(ticker):
    """Checks to see if input ticker is valid"""
    url = f"https://api.iextrading.com/1.0/stock/{ticker}/price"
    r = requests.get(url)
    return r.text == "Unknown symbol"
