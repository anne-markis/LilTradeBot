import asyncio
from dotenv import load_dotenv

from .lil_trade_bot import LilTradeBot

load_dotenv()

async def main():
    await LilTradeBot().run()
    

if __name__ == "__main__":
    asyncio.run(main())
