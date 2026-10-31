# =============================================================
# sentiment.py — Sentiment Analysis Module
# =============================================================
# This file is the "brain" of the project. It uses FinBERT,
# a financial AI model trained specifically on financial news,
# to read text and decide if it is positive, negative, or neutral.
#
# What it does:
#   - analyze_sentiment(text): takes ONE piece of text (e.g. a news
#     headline) and returns:
#       * label: "positive", "negative", or "neutral"
#       * confidence: how sure the model is (0 to 1)
#       * sentiment_score: a score from -1 (very negative)
#         to +1 (very positive)
#
#   - analyze_multiple(texts): takes a LIST of texts, scores each
#     one, and returns an overall average sentiment score for all
#     of them combined.
#
# Why we need it:
#   We feed it the news headlines collected for a stock.
#   It scores each one automatically so we
#   can track whether public opinion is turning positive or
#   negative — without reading anything manually.
#
# Example:
#   "NVIDIA crushes earnings"  → positive | score: +0.94
#   "NVIDIA faces export ban"  → negative | score: -0.96
# =============================================================

from transformers import pipeline

# Load FinBERT model (this is the AI that reads financial text)
finbert = pipeline("text-classification", model="ProsusAI/finbert")

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of a piece of financial text.
    Returns: label (positive/negative/neutral) and confidence score
    """
    result = finbert(text, truncation=True, max_length=512)[0]
    
    label = result["label"]      # positive, negative, or neutral
    score = result["score"]      # confidence between 0 and 1

    # Convert to a -1 to +1 scale
    if label == "positive":
        sentiment_score = score
    elif label == "negative":
        sentiment_score = -score
    else:
        sentiment_score = 0.0

    return {
        "text": text,
        "label": label,
        "confidence": round(score, 4),
        "sentiment_score": round(sentiment_score, 4)
    }

def analyze_multiple(texts: list) -> list:
    """
    Analyze a list of texts and return their average sentiment score.
    """
    results = [analyze_sentiment(t) for t in texts]
    avg_score = sum(r["sentiment_score"] for r in results) / len(results)
    
    return {
        "results": results,
        "average_score": round(avg_score, 4),
        "overall_label": "positive" if avg_score > 0.1 else "negative" if avg_score < -0.1 else "neutral"
    }

# Test it
if __name__ == "__main__":
    headlines = [
        "NVIDIA crushes earnings expectations, revenue up 40%",
        "NVIDIA stock faces pressure amid new export restrictions",
        "NVIDIA announces new partnership with Microsoft"
    ]

    print("--- Testing Individual Headlines ---")
    for headline in headlines:
        result = analyze_sentiment(headline)
        print(f"\nText: {result['text']}")
        print(f"Label: {result['label']} | Score: {result['sentiment_score']}")

    print("\n--- Testing Multiple Headlines Together ---")
    combined = analyze_multiple(headlines)
    print(f"Average Score: {combined['average_score']}")
    print(f"Overall Sentiment: {combined['overall_label']}")