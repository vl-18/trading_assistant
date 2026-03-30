from transformers import pipeline

# Load FinBERT sentiment model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)


def analyze_sentiment(headlines: list[str]) -> dict:
    """
    Returns aggregated sentiment from FinBERT
    """

    if not headlines:
        return {
            "overall_sentiment": "neutral",
            "score": 0.0,
            "confidence": 0.0
        }

    results = sentiment_pipeline(headlines)

    score = 0
    confidence = 0

    for r in results:
        label = r["label"]
        conf = r["score"]

        if label == "positive":
            score += conf
        elif label == "negative":
            score -= conf

        confidence += conf

    avg_score = score / len(results)
    avg_conf = confidence / len(results)

    if avg_score > 0.1:
        sentiment = "positive"
    elif avg_score < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "overall_sentiment": sentiment,
        "score": round(avg_score, 3),
        "confidence": round(avg_conf, 3)
    }