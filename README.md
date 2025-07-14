# LilTradeBot

Simple but opinionated OpenAI LLM helper for deciding which trades to make.

## Method

* Get live portfolio
* Get buy/sell/hold advice on tax loss harvesting
* Get buy/sell/hold advice on upcoming earnings releases
* Have a final opinion that aggregates the information

This is not formal financial advice.

Future improvements:
* Hook into CapitolTrades
* Use Twelvedata (or similar) API to get candlestick data
* Use Newapi (or similar) to get ticker news

### Notes

This bot cannot make trades on your behalf (yet).

Portfolio Source: Robinhood
- They don't actually have a formal API for stock trading, so this API is a little janky. Login may require 2fa.

Broker Source: Robinhood OR Alpaca
- Robinhood if you actually want the bots to make the trades for you
- Alpaca for paper trading

### Install 

```
$ brew install uv OR pip install uv
$ uv sync
```

### Run

In a `.env` set your `OPENAI_API_KEY`

```
$ uv venv
$ source .venv/bin/activate      # or `.venv\Scripts\activate` on Windows
$ python -m liltradebot.main
```


### .env skeleton

```
OPENAI_API_KEY=
PORTFOLIO_SOURCE=robinhood

RH_USERNAME=
RH_PASSWORD=

FINNHUB_KEY=
```