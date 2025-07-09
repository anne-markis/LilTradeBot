
# import requests
# from liltradebot.delme.config import CONFIG
# from bs4 import BeautifulSoup
# import yfinance as yf
# import pandas as pd # TODO want json

# def get_capitol_trades():
#     df = summarize_trades()
#     result = df.to_json
#     print(f"Capitol Trades Result: {result}")
#     return result


# def scrape_trades():
#     url = "https://www.capitoltrades.com/trades?politician=P000197&politician=G000596"
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, "html.parser")
#     rows = soup.select("table tr")[1:]

#     trades = []
#     for row in rows:
#         cols = [td.get_text(strip=True) for td in row.find_all("td")]
#         # Adjust index based on actual table layout:
#         ticker, typ, owner, direction, size = cols[0], cols[1], cols[2], cols[3], cols[4]
#         trades.append(dict(ticker=ticker, type=typ, owner=owner, direction=direction, size=size))
#     return trades

# def get_price(symbol):
#     return yf.Ticker(symbol).info["regularMarketPrice"]

# def summarize_trades():
#     trades = scrape_trades()
#     summary = []
#     for t in trades:
#         try:
#             price = get_price(t["ticker"])
#         except:
#             price = None
#         summary.append({
#             "Symbol": t["ticker"],
#             "Type": t["type"],
#             "Owner": t["owner"],
#             "Direction": t["direction"],
#             "Size Range": t["size"],
#             "Current Price": t["price"]# f"${price:.2f}" if price else "N/A" # TODO this won't work, needs setup in scrape_trades
#         })
#     return pd.DataFrame(summary)