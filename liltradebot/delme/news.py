import requests
from liltradebot.delme.config import CONFIG
from liltradebot.delme.risk_control import is_symbol_allowed

def get_news(symbol):
    headlines = {}
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={CONFIG['newsapi_key']}"
    res = requests.get(url)
    if res.ok:
        headlines[symbol] = res.json().get("articles", [])
    return headlines