import requests
from typing import Any
from liltradebot.delme.config import CONFIG
from liltradebot.broker.base import BaseBroker

class AlpacaBroker(BaseBroker):
    def __init__(self):
        self.key_id = CONFIG["alpaca"]["key_id"]
        self.secret_key = CONFIG["alpaca"]["secret_key"]
        self.base_url = CONFIG["alpaca"]["paper_base_url"]
        self.headers = {
            "APCA-API-KEY-ID": self.key_id,
            "APCA-API-SECRET-KEY": self.secret_key
        }

    def login(self):
        # No explicit login needed for Alpaca
        pass

    # TODO unimplemented
    def get_holdings(self):
        pass

    def place_order(self, symbol: str, side: str, quantity: int = 1):
        order = {
            "symbol": symbol,
            "qty": quantity,
            "side": side.lower(),
            "type": "market",
            "time_in_force": "gtc"
        }
        response = requests.post(f"{self.base_url}/v2/orders", json=order, headers=self.headers)
        if response.ok:
            print(f"[Alpaca] Order placed: {side} {quantity} {symbol}")
        else:
            print(f"[Alpaca] Order failed: {response.text}")
