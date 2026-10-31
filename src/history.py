# history.py - daily news sentiment vs. stock price over a date range

import os
from datetime import date, timedelta

import pandas as pd

from scraper import get_news_for_day
from sentiment import analyze_sentiment
from stocks import get_stock_history

def collect_daily_headlines(ticker: str, company_name: str,
                            start: date, end: date, path: str) -> pd.DataFrame:
    """
    Fetch and score the headlines for every day from start to end.
    If the CSV at `path` already exists, load it instead of calling the API.
    """
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["published"])

    rows = []
    day = start
    while day <= end:
        articles = get_news_for_day(ticker, company_name, day.isoformat())
        for article in articles:
            scored = analyze_sentiment(article["text"])
            rows.append({
                "published": article["published"],
                "label": scored["label"],
                "sentiment_score": scored["sentiment_score"],
                "text": article["text"]
            })
        print(f"{day}: {len(articles)} headlines")
        day += timedelta(days=1)

    headlines = pd.DataFrame(rows)
    headlines["published"] = pd.to_datetime(headlines["published"])

    os.makedirs(os.path.dirname(path), exist_ok=True)
    headlines.to_csv(path, index=False)
    return headlines

def compare_with_price(headlines: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Average the sentiment per trading day and join it with the price.
    News from weekends and holidays counts toward the next trading day,
    since that is the first day the market can react to it.
    """
    history = get_stock_history(ticker, "3mo").reset_index()
    history["Date"] = history["Date"].dt.tz_localize(None).dt.normalize()
    history["price_change_pct"] = history["Close"].pct_change() * 100
    history["next_day_change_pct"] = history["price_change_pct"].shift(-1)

    trading_days = history["Date"].to_numpy()
    positions = trading_days.searchsorted(headlines["published"].to_numpy())
    headlines = headlines[positions < len(trading_days)].copy()
    headlines["trading_day"] = trading_days[positions[positions < len(trading_days)]]

    daily = headlines.groupby("trading_day").agg(
        sentiment=("sentiment_score", "mean"),
        headlines=("sentiment_score", "size"),
        positive=("label", lambda s: (s == "positive").sum()),
        negative=("label", lambda s: (s == "negative").sum()),
        neutral=("label", lambda s: (s == "neutral").sum())
    ).reset_index().rename(columns={"trading_day": "Date"})

    daily = daily.merge(
        history[["Date", "Close", "price_change_pct", "next_day_change_pct"]],
        on="Date", how="inner"
    )
    return daily

# Test
if __name__ == "__main__":
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=6)
    headlines = collect_daily_headlines("NVDA", "NVIDIA", start, end, "data/test_headlines.csv")
    print(compare_with_price(headlines, "NVDA"))
