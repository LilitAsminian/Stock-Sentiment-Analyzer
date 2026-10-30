# =============================================================
# stocks.py — Stock Price Module
# =============================================================
# This file is responsible for fetching real stock market data
# from the internet using the yfinance library (Yahoo Finance).
#
# What it does:
#   - get_stock_price(ticker): fetches the CURRENT live price
#     of a stock (e.g. NVDA, AAPL, TSLA) along with basic info
#     like day high, day low, volume, and company name.
#
#   - get_stock_history(ticker, period): fetches HISTORICAL price
#     data for the last N days/months so we can see how the stock
#     moved over time.
#
# Why we need it:
#   After we analyze the sentiment of news headlines, we compare
#   that sentiment against the actual stock price movements to see
#   if positive/negative news actually impacted the price.
#
# Example usage:
#   get_stock_price("NVDA")  → returns current NVIDIA price
#   get_stock_history("NVDA", "7d") → returns last 7 days of data
# =============================================================


import yfinance as yf
import pandas as pd

def get_stock_price(ticker: str) -> dict:
    """
    Fetch current stock price and basic info for a given ticker.
    Example: get_stock_price("NVDA")
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker,
        "current_price": info.get("currentPrice"),
        "previous_close": info.get("previousClose"),
        "day_high": info.get("dayHigh"),
        "day_low": info.get("dayLow"),
        "volume": info.get("volume"),
        "company_name": info.get("longName")
    }

def get_stock_history(ticker: str, period: str = "7d") -> pd.DataFrame:
    """
    Fetch historical price data for a given ticker.
    Period options: 1d, 5d, 7d, 1mo, 3mo, 6mo, 1y
    """
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)
    return history

# Test it
if __name__ == "__main__":
    data = get_stock_price("NVDA")
    print(data)

    history = get_stock_history("NVDA")
    print(history)