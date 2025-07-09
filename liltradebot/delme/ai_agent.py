from openai import OpenAI
from pydantic import BaseModel
from liltradebot.delme.config import CONFIG

class TradeOpinion(BaseModel):
    result: str
    explanation: str

# TODO: Add weight for each information source; add in other market indiciators like RSI, MACD, etc.
# TODO would be fun to use agents that specialize in each data source to give a singular opinion
# TODO removed Capitol Trades: {data['capitol_trades']}
# TODO tax loss harvest agent
def get_trade_opinion(symbol, data):
    client = OpenAI(api_key=CONFIG["openai_key"])

    prompt = f"""
    Based on the following data for {symbol}, suggest whether to buy, sell, or hold:

    News: {data['news']}
    Price Data: {data['candles']}

    Respond with a one-word decision (BUY/SELL/HOLD) and one short sentence explanation.
    Valid responses for 'result' are BUY or SELL or HOLD only (no additional formatting)
    """

    response = client.responses.parse(
        model="gpt-4o-mini", # TODO configurable
        input=prompt,
        text_format=TradeOpinion,
    )

    return response.output_parsed
