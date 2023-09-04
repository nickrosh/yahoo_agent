from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type, List
from api_functions import (
    get_todays_price, 
    get_best_performing, 
    get_price_change_percent,
    get_simple_moving_average,
    get_exponential_moving_average,
    )


class StockPriceCheckInput(BaseModel):
    """Input for stock price check."""
    stockticker: str = Field(..., description='Ticker symbol for stock or index')


class StockPriceTool(BaseTool):
    name = 'get_stock_ticker_price'
    description = 'Useful for when you need to find out the price of a stock. You should input the stock ticker used on the yfinance API'

    def _run(self, stockticker: str):
        price_resonse = get_todays_price(stockticker)
        return price_resonse
    
    def _arun(self, stockticker: str):
        raise NotImplementedError('This tool does not support Async')
    
    args_schema: Optional[Type[BaseModel]] = StockPriceCheckInput


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


class StockSMAInput(BaseModel):
    """Input for Stock simple moving average. For SMA"""

    stockticker: str = Field(..., description='Ticker symbol for stock or index')
    days_ago: int = Field(..., description='Int number of days to look back')
    span: int = Field(..., description='Int number of days for moving average')


class StockSMATool(BaseTool):
    name = 'get_simple_moving_average'
    description = "Useful for when you need to find out the percent change of the simple moving average of a stock's price. You should input the stock ticker used on the yfinance API and also input the number of days to check the change over and also input the time span for the moving average"

    def _run(self, stockticker: str, days_ago: int, span: int):
        price_change_response = get_simple_moving_average(stockticker, days_ago, span)
        return price_change_response
    
    def _arun(self, stockricker: str, days_ago: int, span: int):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = StockSMAInput


class StockEMAInput(BaseModel):
    """Input for Stock exponential moving average. For EMA"""

    stockticker: str = Field(..., description='Ticker symbol for stock or index')
    days_ago: int = Field(..., description='Int number of days to look back')
    span: int = Field(..., description='Int number of days for moving average')


class StockEMATool(BaseTool):
    name = 'get_exponential_moving_average'
    description = "Useful for when you need to find out the percent change of the exponential moving average of a stock's price. You should input the stock ticker used on the yfinance API and also input the number of days to check the change over and also input the time span for the moving average"

    def _run(self, stockticker: str, days_ago: int, span: int):
        price_change_response = get_exponential_moving_average(stockticker, days_ago, span)
        return price_change_response
    
    def _arun(self, stockricker: str, days_ago: int, span: int):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = StockEMAInput
