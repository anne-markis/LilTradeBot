from typing import List, Optional, Any
from agents import Runner, Agent
from pydantic import BaseModel
from liltradebot.broker import get_portfolio_source, get_broker

MODEL_NAME="gpt-4o-mini"

portfolio_temp = """
{
  "SPY": {
    "price": "619.979900",
    "quantity": "13.58671600",
    "average_buy_price": "319.9465",
    "equity": "8423.49",
    "percent_change": "93.78",
    "intraday_percent_change": "0.00",
    "equity_change": "4076.468596",
    "type": "etp",
    "name": "SPDR S&P 500 ETF",
    "id": "8f92e76f-1e0e-4478-8580-16a6ffcfaef5",
    "pe_ratio": "27.249327",
    "percentage": "16.02"
  },
  "SMOG": {
    "price": "110.975000",
    "quantity": "13.65457500",
    "average_buy_price": "61.2776",
    "equity": "1515.32",
    "percent_change": "81.10",
    "intraday_percent_change": "0.00",
    "equity_change": "678.596876",
    "type": "etp",
    "name": "VanEck Low Carbon Energy ETF",
    "id": "5fd916aa-d4a0-4eb7-b3ee-533d0fb5a8bb",
    "pe_ratio": "56.409397",
    "percentage": "2.88"
  },
  "XLF": {
    "price": "52.510000",
    "quantity": "19.22161900",
    "average_buy_price": "33.5284",
    "equity": "1009.33",
    "percent_change": "56.61",
    "intraday_percent_change": "0.00",
    "equity_change": "364.857083",
    "type": "etp",
    "name": "Financial Select Sector SPDR Fund",
    "id": "f25b2d63-0372-4827-9907-e7e9e37a10f1",
    "pe_ratio": "19.128424",
    "percentage": "1.92"
  },
  "SHE": {
    "price": "124.905000",
    "quantity": "10.59795600",
    "average_buy_price": "67.5364",
    "equity": "1323.74",
    "percent_change": "84.94",
    "intraday_percent_change": "0.00",
    "equity_change": "607.989899",
    "type": "etp",
    "name": "SPDR MSCI USA Gender Diversity ETF",
    "id": "7241f3e4-e160-4b73-9559-2cc6a19ff4c5",
    "pe_ratio": "26.036842",
    "percentage": "2.52"
  },
  "PBW": {
    "price": "21.290000",
    "quantity": "14.54076400",
    "average_buy_price": "25.2079",
    "equity": "309.57",
    "percent_change": "-15.54",
    "intraday_percent_change": "0.00",
    "equity_change": "-56.969259",
    "type": "etp",
    "name": "Invesco WilderHill Clean Energy ETF",
    "id": "0301c923-0af3-4be3-8f48-15b4ff4ff84c",
    "pe_ratio": "-8.083506",
    "percentage": "0.59"
  },
  "TSLA": {
    "price": "295.590000",
    "quantity": "16.89797000",
    "average_buy_price": "20.3000",
    "equity": "4994.87",
    "percent_change": "1356.11",
    "intraday_percent_change": "0.00",
    "equity_change": "4651.842161",
    "type": "stock",
    "name": "Tesla",
    "id": "e39ed23a-7bd1-4587-b060-71988d9ef483",
    "pe_ratio": "173.421689",
    "percentage": "9.50"
  },
  "IWF": {
    "price": "425.300000",
    "quantity": "9.65184100",
    "average_buy_price": "224.7882",
    "equity": "4104.93",
    "percent_change": "89.20",
    "intraday_percent_change": "0.00",
    "equity_change": "1935.308012",
    "type": "etp",
    "name": "iShares Russell 1000 Growth ETF",
    "id": "42ee895d-4b4e-4bc3-a539-553b021d85c9",
    "pe_ratio": "39.776380",
    "percentage": "7.81"
  }
}
"""

class LilTradeBot:
    def __init__(self):
        print("Starting Lil Trade Bot...")
        self.portfolio_source = get_portfolio_source()
        self.portfolio_source.login()
        print(f"Successfully logged into portfolio source {self.portfolio_source}...")
        # self.broker = get_broker()
        # print(f"[LIES] Successfully logged into broker source {self.broker}...")

    async def run(self) -> None:
        portfolio = self.portfolio_source.get_holdings()
        print(f"{portfolio}")

        tax_loss_harvesting_opinion = await self._tax_loss_havesting_opinion(portfolio)
        print(f"plan {tax_loss_harvesting_opinion}")


    async def _tax_loss_havesting_opinion(self, portfolio: str) -> Any:
        result = await Runner.run(
            tax_loss_harvesting_agent,
            f"{portfolio}",
        )
        print(f"{result}")


##### TAX HARVESTING ######

TAX_HARVESTING_PROMPT = (
"""
You are a financial advisor AI agent specializing in tax-loss harvesting strategy.

Your task is to:
- Analyze the user's portfolio.
- Identify underperforming assets with unrealized losses.
- Recommend which assets to sell to realize capital losses.
- Avoid suggesting any assets that could trigger wash sale rules.
- Optionally recommend replacements that have similar exposure but are not substantially identical.
"""
)



class SellRecommendation(BaseModel):
    symbol: str
    quantity: int
    loss: float
    reason: Optional[str] = None


class BuyAlternative(BaseModel):
    replacement_for: str
    symbol: str
    quantity: str
    justification: Optional[str] = None


class TaxLossRecommendations(BaseModel):
    sell: List[SellRecommendation]
    buy_alternatives: List[BuyAlternative]


class TaxLossHarvestingOpinions(BaseModel):
    recommendations: TaxLossRecommendations


tax_loss_harvesting_agent = Agent(
    name="tax_loss_havesting_agent",
    instructions=TAX_HARVESTING_PROMPT,
    model=MODEL_NAME,
    output_type=TaxLossHarvestingOpinions,
)
