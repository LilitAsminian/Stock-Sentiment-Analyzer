# =============================================================
# pipeline.py — Main Pipeline Module
# =============================================================
# This file connects all 3 modules together into one flow:
#
#   1. scraper.py   → collect headlines for a stock
#   2. sentiment.py → score each headline
#   3. stocks.py    → fetch current price
#   4. Save everything into a combined result
#
# This is the file that runs the full analysis for any stock
# in one single function call.
# =============================================================

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import get_news
from sentiment import analyze_multiple
from stocks import get_stock_price, get_stock_history
from datetime import datetime

def run_analysis(ticker: str, company_name: str = "") -> dict:
    """
    Run the full sentiment + price analysis for a stock.
    Returns a combined result dictionary.
    """
    print(f"\n{'='*50}")
    print(f"Running analysis for {ticker}...")
    print(f"{'='*50}")

    # Step 1 — Collect headlines
    print("\n[1/3] Fetching headlines...")
    headlines = get_news(ticker, company_name)
    print(f"      Found {len(headlines)} headlines")

    # Step 2 — Score sentiment
    print("\n[2/3] Analyzing sentiment...")
    sentiment = analyze_multiple(headlines)
    print(f"      Average score: {sentiment['average_score']}")
    print(f"      Overall sentiment: {sentiment['overall_label']}")

    # Step 3 — Fetch stock price
    print("\n[3/3] Fetching stock price...")
    price = get_stock_price(ticker)
    print(f"      Current price: ${price['current_price']}")

    # Combine everything
    result = {
        "ticker": ticker,
        "company_name": price["company_name"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "current_price": price["current_price"],
        "previous_close": price["previous_close"],
        "day_high": price["day_high"],
        "day_low": price["day_low"],
        "sentiment_score": sentiment["average_score"],
        "sentiment_label": sentiment["overall_label"],
        "headlines_analyzed": len(headlines),
        "headlines": sentiment["results"]
    }

    return result

# Test it
if __name__ == "__main__":
    result = run_analysis("NVDA", "NVIDIA")

    print(f"\n{'='*50}")
    print(f"FINAL RESULT FOR {result['ticker']}")
    print(f"{'='*50}")
    print(f"Company:          {result['company_name']}")
    print(f"Time:             {result['timestamp']}")
    print(f"Current Price:    ${result['current_price']}")
    print(f"Previous Close:   ${result['previous_close']}")
    print(f"Sentiment Score:  {result['sentiment_score']}")
    print(f"Sentiment Label:  {result['sentiment_label']}")
    print(f"Headlines Analyzed: {result['headlines_analyzed']}")