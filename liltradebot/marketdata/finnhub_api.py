import os
from datetime import datetime, timedelta
import finnhub


def get_earnings_calendar_for_symbols(portfolio):
    """
    Fetches and updates the earnings calendar for stock symbols in the given portfolio.

    This function iterates through the provided portfolio, identifies symbols of type "stock",
    and retrieves their upcoming earnings calendar events using the Finnhub API. The earnings
    data is fetched for a window starting 15 days before today and ending 30 days after today.
    The retrieved earnings information is then assigned to the corresponding symbol's `earnings`
    attribute in the portfolio.

    Args:
        portfolio (dict): A dictionary of symbol objects, where each symbol object should have
            a `type` attribute (e.g., "stock") and an `earnings` attribute to store the results.

    Returns:
        dict: The updated portfolio dictionary with the `earnings` attribute populated for each
            stock symbol.
    """
    finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_KEY"))

    today = datetime.now()
    start_date = today - timedelta(days=15)
    end_date = today + timedelta(days=30)

    for symbol, data in portfolio.items():
        if data.get("type") == "stock":
            earnings = finnhub_client.earnings_calendar(_from=start_date.strftime("%Y-%m-%d"), to=end_date.strftime("%Y-%m-%d"), symbol=symbol, international=False)
            data.update(earnings)
            # portfolio[s]['earnings'] = data
    return portfolio
    
