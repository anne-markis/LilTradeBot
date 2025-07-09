import requests
from liltradebot.delme.config import CONFIG
import datetime

def get_candlestick_data(symbol):
    now = datetime.datetime.utcnow()
    one_hour_ago = now - datetime.timedelta(hours=1)

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}&interval=1min&start_date={one_hour_ago.isoformat()}&apikey={CONFIG['twelvedata_key']}"
    )

    res = requests.get(url)
    return res.json() if res.ok else {}

