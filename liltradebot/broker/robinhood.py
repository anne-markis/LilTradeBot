import os
from typing import Any
import robin_stocks.robinhood as r
from liltradebot.broker.base import BaseBroker

# TODO requires 2fa to login
class RobinhoodBroker(BaseBroker):
    def login(self):
        username = os.getenv("RH_USERNAME")
        password = os.getenv("RH_PASSWORD")

        r.login(username, password)

    def get_holdings(self) -> Any:
        self.login()
        return r.build_holdings()

    def place_order(self, symbol: str, side: str, quantity: int = 1):
        if side.lower() == "buy":
            order = r.orders.order_buy_market(symbol, quantity)
        elif side.lower() == "sell":
            order = r.orders.order_sell_market(symbol, quantity)
        else:
            print(f"[Robinhood] Invalid order side: {side}")
            return

        if order:
            print(f"[Robinhood] Order placed: {side} {quantity} {symbol}")
        else:
            print(f"[Robinhood] Order failed.")
