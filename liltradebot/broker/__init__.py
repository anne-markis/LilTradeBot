import os
from liltradebot.broker.robinhood import RobinhoodBroker
from liltradebot.broker.alpaca import AlpacaBroker

def get_broker():
    broker_source = os.getenv("TRADING_BROKER_SOURCE")
    match broker_source:
        case "alpaca":
            return AlpacaBroker()
        case "robinhood":
            return RobinhoodBroker()
        case _:
            print(f"Unsupported broker source")
            raise ValueError(f"Unsupported broker: {broker_source}")


def get_portfolio_source():
    portfolio_source = os.getenv("PORTFOLIO_SOURCE")
    match portfolio_source:
        case "robinhood":
            return RobinhoodBroker()
        case _:
            print(f"Unsupported portfolio source")
            raise ValueError(f"Unsupported portfolio source: {portfolio_source}")

    