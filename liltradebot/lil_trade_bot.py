from typing import List, Optional, Any
from agents import Runner, Agent
from pydantic import BaseModel
from liltradebot.broker import get_portfolio_source
from .marketdata.finnhub_api import get_earnings_calendar_for_symbols

MODEL_NAME="gpt-4o-mini"


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

        portfolio_with_earnings = get_earnings_calendar_for_symbols(portfolio)
        earnings_opinion = await self._earnings_opinions(portfolio_with_earnings)

        tax_loss_harvesting_opinion = await self._tax_loss_havesting_opinion(portfolio)

        final_opinion = await self._final_opinion(portfolio, earnings_opinion, tax_loss_harvesting_opinion)
        print(f"FINAL OPINION: {final_opinion}")

    async def _final_opinion(self, portfolio: str, earnings_opinion:str, tax_loss_harvesting_opinion: str):
        result = await Runner.run(
            boss_agent,
            f"""
Portfolio: {portfolio}

Earnings Opinion: {earnings_opinion}

Tax Loss Harvesting Opinion: {tax_loss_harvesting_opinion}
""",
        )
        return result
    
    async def _tax_loss_havesting_opinion(self, portfolio: str) -> Any:
        result = await Runner.run(
            tax_loss_harvesting_agent,
            f"{portfolio}",
        )
        #print(f"{result}")

    async def _earnings_opinions(self, earnings: str) -> Any:
        result = await Runner.run(
            earnings_agent,
            f"{earnings}",
        )
        # print(f"{result}")
##### BOSS AGENT ######
BOSS_PROMPT = (
"""
You have the final word on what goes into a report out to investors on how to rebalance their portfolio.
You are mildly risk averse and err on the side of data to make decisions.

Your task is to:
- Read the incoming trade opinions from employees
- Aggregate the reports to form a final opinion
- Organize a final buy/sell/hold opinion
- Uplevel information to the investor that they should keep an eye on, such as upcoming earnings dates
""" 
)

class Notable(BaseModel):
    symbol: str
    earnings_date: str
    reason: Optional[str] = None


class EarningsReco(BaseModel):
    symbol: str
    quantity: str
    earnings_date: str
    justification: Optional[str] = None

class EarningsRecommendations(BaseModel):
    upcoming_earnings: List[Notable]
    buy: List[EarningsReco]
    sell: List[EarningsReco]
    wait: List[EarningsReco]


class BossOpinions(BaseModel):
    recommendations: EarningsRecommendations

boss_agent = Agent(
    name="boss_agent",
    instructions=BOSS_PROMPT,
    model=MODEL_NAME,
    output_type=BossOpinions,
)
  

##### EARNINGS REPORTS #####
EARNINGS_PROMPT = (
"""
You are a financial analyst tasked at looking at earnings.
Your goal is to identify stocks that have earnings reports coming up and recommend trade opportunities.

Your task is to:
- Analyze stock's earnings schedule
- Identify underperforming assets with upcoming earnings
- Identify overperforming assets with upcoming earnings
- Highlight any stocks that would be especially interesting to keep an eye on
"""
)

class EarningsOpinions(BaseModel):
    recommendations: EarningsRecommendations



earnings_agent = Agent(
    name="earnings_agent",
    instructions=EARNINGS_PROMPT,
    model=MODEL_NAME,
    output_type=EarningsOpinions,
)
  


##### TAX HARVESTING ######

TAX_HARVESTING_PROMPT = (
"""
You are a financial advisor AI agent specializing in tax-loss harvesting strategy.
Your goal is to analyze a given portfolio and identify opportunities for tax loss harvesting.

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
