import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "broker": os.getenv("TRADING_BROKER", "alpaca"),  # Default to alpaca
    "alpaca": {
        "key_id": os.getenv("ALPACA_KEY_ID"),
        "secret_key": os.getenv("ALPACA_SECRET_KEY"),
        "paper_base_url": os.getenv("ALPACA_PAPER_BASE_URL", "https://paper-api.alpaca.markets")
    },
    "robinhood": {
        "username": os.getenv("RH_USERNAME"),
        "password": os.getenv("RH_PASSWORD")
    },
    "openai_key": os.getenv("OPENAI_API_KEY"),
    "newsapi_key": os.getenv("NEWSAPI_KEY"),
    "twelvedata_key": os.getenv("TWELVEDATA_KEY"),
    "limits": {
        "allowed_symbols": os.getenv("ALLOWED_SYMBOLS", "").split(",")  # e.g. "AAPL,SPY"
    },
}
