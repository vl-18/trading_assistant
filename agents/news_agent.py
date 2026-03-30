from app.state import NewsData, SentimentOutput
from features.sentiment import analyze_sentiment
from agents.utils import call_llm
import json


SUMMARY_PROMPT = """
You are a financial news analyst.

Given these headlines:
{headlines}

Summarize the key market sentiment in 1-2 lines.

Return ONLY JSON:
{{
  "summary": "your summary here"
}}
"""


def news_agent(news: NewsData) -> SentimentOutput:
    """
    Combines FinBERT + LLM summary
    """

    # Step 1: FinBERT sentiment
    sentiment_data = analyze_sentiment(news.headlines)

    # Step 2: LLM summary
    prompt = SUMMARY_PROMPT.format(
        headlines="\n".join(news.headlines[:5])  # limit for cost
    )

    response = call_llm(prompt)

    try:
        parsed = json.loads(response)
        summary = parsed.get("summary", "")
    except:
        summary = "Summary unavailable"

    # Step 3: Combine into schema
    return SentimentOutput(
        overall_sentiment=sentiment_data["overall_sentiment"],
        score=sentiment_data["score"],
        confidence=sentiment_data["confidence"],
        summary=summary
    )