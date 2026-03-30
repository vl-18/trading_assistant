from models.predict import predict
from app.state import (
    TechnicalIndicators,
    NewsData
)
from agents.market_agent import market_agent
from agents.news_agent import news_agent
from agents.decision_agent import decision_agent
from strategy.guard import strategy_guard

import yfinance as yf


def get_technicals(symbol: str) -> TechnicalIndicators:
    """
    Fetch latest technical indicators from market data
    """

    df = yf.download(symbol, period="3mo", interval="1d")

    # Compute same features as ML
    df["ema20"] = df["Close"].ewm(span=20).mean()
    df["ema50"] = df["Close"].ewm(span=50).mean()

    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    ema12 = df["Close"].ewm(span=12).mean()
    ema26 = df["Close"].ewm(span=26).mean()
    df["macd"] = ema12 - ema26

    df.dropna(inplace=True)

    latest = df.iloc[-1]

    return TechnicalIndicators(
        rsi=float(latest["rsi"].iloc[0]),
        ema20=float(latest["ema20"].iloc[0]),
        ema50=float(latest["ema50"].iloc[0]),
        macd=float(latest["macd"].iloc[0]),
        volume=float(latest["Volume"].iloc[0])
    )


def get_news(symbol: str) -> NewsData:
    """
    TEMP: Mock news (replace later with real API)
    """

    return NewsData(headlines=[
        f"{symbol} shows recent market movement",
        f"Investors reacting to latest trends in {symbol}",
        f"Sector outlook remains uncertain"
    ])


def get_risk() -> dict:
    """
    TEMP: simple risk logic (replace later with agent)
    """

    return {
        "risk_level": "medium",
        "position_size": 0.02,
        "stop_loss": 0.03,
        "take_profit": 0.05,
        "warning": "Normal conditions"
    }


def run_pipeline(symbol: str = "TCS.NS"):
    print(f"\n📊 Running pipeline for {symbol}\n")

    # =========================
    # 1. ML Prediction
    # =========================
    ml_output = predict(symbol)
    print("ML Output:", ml_output)

    # =========================
    # 2. Market Agent
    # =========================
    technicals = get_technicals(symbol)
    market = market_agent(technicals)
    print("Market Analysis:", market)

    # =========================
    # 3. News Agent
    # =========================
    news = get_news(symbol)
    sentiment = news_agent(news)
    print("Sentiment:", sentiment)

    # =========================
    # 4. Risk (mock)
    # =========================
    risk_dict = get_risk()

    # Convert to schema
    from app.state import RiskAnalysis
    risk = RiskAnalysis(**risk_dict)

    print("Risk:", risk)

    # =========================
    # 5. Decision Agent
    # =========================
    decision = decision_agent(
        ml_output,
        market,
        sentiment,
        risk
    )
    print("Decision:", decision)

    # =========================
    # 6. Strategy Guard (FINAL)
    # =========================
    final = strategy_guard(
        ml_output,
        market,
        sentiment,
        risk,
        decision
    )

    print("\n🚀 FINAL SIGNAL:", final)
    return final


if __name__ == "__main__":
    run_pipeline("TCS.NS")