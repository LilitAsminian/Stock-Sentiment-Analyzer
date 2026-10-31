# =============================================================
# scraper.py — Data Collection Module
# =============================================================
# This file is responsible for automatically collecting news
# headlines about any stock from the internet.
# Think of it as a robot that reads the news so you don't have to.
#
# What it will do:
#   - get_news(ticker): searches NewsAPI for the latest news
#     articles mentioning a stock (e.g. "NVIDIA") and returns
#     a list of headlines from thousands of news sources.
#
# Why we need it:
#   Instead of manually typing headlines into sentiment.py,
#   this file automatically collects the latest real headlines
#   on every run. Those headlines are then passed to sentiment.py
#   to be scored, and the scores are compared against stock
#   prices from stocks.py.
#
# This is what connects everything together:
#   scraper.py (collect) → sentiment.py (score) → stocks.py (compare)
# =============================================================

import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize the NewsAPI client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_news(ticker: str, company_name: str = "") -> list:
    """
    Fetch latest news headlines for a stock ticker.
    Returns a list of headlines as strings.
    """
    # Search using both ticker and company name for better results
    query = f"{ticker} {company_name} stock".strip()

    response = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="publishedAt",  # most recent first
        page_size=20            # fetch 20 headlines at a time
    )

    headlines = []
    for article in response["articles"]:
        title = article["title"]
        description = article["description"]

        # Use description if available, otherwise just title
        text = f"{title}. {description}" if description else title
        headlines.append(text)

    return headlines


def get_news_for_day(ticker: str, company_name: str, day: str) -> list:
    """
    Fetch up to 100 headlines published on one day (YYYY-MM-DD)
    that mention the company or ticker in the title.
    Returns a list of dicts with the publish date and text.
    """
    response = newsapi.get_everything(
        qintitle=f"{company_name} OR {ticker}",
        language="en",
        from_param=day,
        to=day,
        page_size=100
    )

    articles = []
    for article in response["articles"]:
        if article["publishedAt"][:10] != day:
            continue
        title = article["title"]
        description = article["description"]
        text = f"{title}. {description}" if description else title
        articles.append({"published": day, "text": text})

    return articles


# Test
if __name__ == "__main__":
    print("--- Fetching News for NVIDIA ---")
    headlines = get_news("NVDA", "NVIDIA")

    for i, headline in enumerate(headlines, 1):
        print(f"\n{i}. {headline}")

    print(f"\nTotal headlines fetched: {len(headlines)}")