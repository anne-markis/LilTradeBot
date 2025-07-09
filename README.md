# LilTradeBot

Simple but opinionated OpenAI LLM helper for deciding which trades to make.

This is not formal financial advice.

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

TODO fill out

```
OPENAI_API_KEY=

```