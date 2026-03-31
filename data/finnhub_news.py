import finnhub
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.state import NewsData

load_dotenv()

client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))


def get_news_finnhub(symbol: str) -> NewsData:
    """
    Fetch company news using Finnhub SDK
    """

    query = symbol.split(".")[0]  # TCS.NS → TCS

    today = datetime.today()
    week_ago = today - timedelta(days=7)

    try:
        data = client.company_news(
            query,
            _from=week_ago.strftime("%Y-%m-%d"),
            to=today.strftime("%Y-%m-%d")
        )
    except Exception as e:
        print("❌ Finnhub error:", e)
        return NewsData(headlines=["Error fetching news"])

    headlines = []

    for article in data:
        title = article.get("headline", "")
        summary = article.get("summary", "")

        # Combine both for better sentiment
        text = f"{title}. {summary}".strip()

        if len(text) > 30:
            headlines.append(text)

    # Deduplicate
    headlines = list(set(headlines))

    # 🚨 Important fallback (VERY IMPORTANT)
    if not headlines:
        return get_general_news()
    print("\n📰 Headlines:")
    for h in headlines:
        print("-", h[:120])

    return NewsData(headlines=headlines[:5])


def get_general_news() -> NewsData:
    """
    Fallback to general market news
    """

    try:
        data = client.general_news('general')
    except Exception as e:
        print("❌ General news error:", e)
        return NewsData(headlines=["Error fetching news"])

    headlines = []

    for article in data[:10]:
        text = f"{article.get('headline', '')}. {article.get('summary', '')}"
        headlines.append(text)
    
    print("\n📰 Headlines:")
    for h in headlines:
        print("-", h[:120])
    return NewsData(headlines=headlines[:5])