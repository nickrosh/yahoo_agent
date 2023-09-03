import os
from typing import List
from datetime import datetime, timedelta

from dotenv import load_dotenv
import yfinance as yf
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv(override=True)

# Stock Price
def get_stock_df(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='7d')
    return todays_data

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return round(todays_data['Close'][0], 2)


class StockPriceCheckInput(BaseModel):
    """Input for stock price check."""
    stockticker: str = Field(..., description='Ticker symbol for stock or index')


class StockPriceTool(BaseTool):
    name = 'get_stock_ticker_price'
    description = 'Useful for when you need to find out the price of a stock. You should input the stock ticker used on the yfinance API'

    def _run(self, stockticker: str):
        # print("I'm running")
        price_resonse = get_stock_price(stockticker)
        return price_resonse
    
    def _arun(self, stockticker: str):
        raise NotImplementedError('This tool does not support Async')
    
    args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput


# Percent Change
def get_price_change_percent(symbol, days_ago):
    ticker = yf.Ticker(symbol)

    # Get today's date
    end_date = datetime.now()

    # Get the date N days ago
    start_date = end_date - timedelta(days=days_ago)

    # Convert dates to string format that yfinance can accept
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    # Get the historical data
    historical_data = ticker.history(start=start_date, end=end_date)

    # Get the closing price N days ago and today's closing price
    old_price = historical_data['Close'].iloc[0]
    new_price = historical_data['Close'].iloc[-1]

    # Calculate the percentage change
    percent_change = ((new_price - old_price) / old_price) * 100

    return round(percent_change, 2)


class StockChangePercentageCheckInput(BaseModel):
    """Input for Stock ticker check. For percentage check"""

    stockticker: str = Field(..., description='Ticker symbol for stock or index')
    days_ago: int = Field(..., description='Int number of days to look back')


class StockPercentageChangeTool(BaseTool):
    name = 'get_price_change_percent'
    description = "Useful for when you need to find out the percentage change in a stock's value. You should input the stock ticker used on the yfinance API and also input the number of days to check the change over"

    def _run(self, stockticker: str, days_ago: int):
        price_change_response = get_price_change_percent(stockticker, days_ago)
        return price_change_response
    
    def _arun(self, stockricker: str, days_ago: int):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = StockChangePercentageCheckInput


# The best performing
def calculate_performance(symbol, days_ago):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    historical_data = ticker.history(start=start_date, end=end_date)
    old_price = historical_data['Close'].iloc[0]
    new_price = historical_data['Close'].iloc[-1]
    percent_change = ((new_price - old_price) / old_price) * 100
    return round(percent_change, 2)


def get_best_performing(stocks, days_ago):
    best_stock = None
    best_performance = None
    for stock in stocks:
        try:
            performance = calculate_performance(stock, days_ago)
            if best_performance is None or performance > best_performance:
                best_stock = stock
                best_performance = performance
        except Exception as e:
            print(f'Couls not caluclate performance for {stock}: {e}')
    return best_stock, best_performance


class StockBestPerformingInput(BaseModel):
    """Input for Stock ticker check. For percentage check"""

    stocktickers: List[str] = Field(..., description="Ticker symbols for stocks or indices")
    days_ago: int = Field(..., description="Int number of days to look back")


class StockGetBestPerformingTool(BaseTool):
    name = "get_best_performing"
    description = "Useful for when you need to the performance of multiple stocks over a period. You should input a list of stock tickers used on the yfinance API and also input the number of days to check the change over"

    def _run(self, stocktickers: List[str], days_ago: int):
        price_change_response = get_best_performing(stocktickers, days_ago)
        return price_change_response
    
    def _arun(self, stocktickers: List[str], days_ago: int):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = StockBestPerformingInput


tools = [StockPriceTool(), StockPercentageChangeTool(), StockGetBestPerformingTool()]
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0613')
open_ai_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)
open_ai_agent.run("how much has google's stock gone up in the last three months?")