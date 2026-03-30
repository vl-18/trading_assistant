import yfinance as yf
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from app.state import MLOutput


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute basic technical indicators
    """

    df["returns"] = df["Close"].pct_change()

    # RSI
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # EMA
    df["ema20"] = df["Close"].ewm(span=20).mean()
    df["ema50"] = df["Close"].ewm(span=50).mean()

    # MACD
    ema12 = df["Close"].ewm(span=12).mean()
    ema26 = df["Close"].ewm(span=26).mean()
    df["macd"] = ema12 - ema26

    df.dropna(inplace=True)

    return df


def prepare_data(df: pd.DataFrame):
    """
    Create features and target
    """

    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    features = ["rsi", "ema20", "ema50", "macd", "Volume"]

    X = df[features]
    y = df["target"]

    return X, y


def predict(symbol: str = "TCS.NS") -> MLOutput:
    """
    Train simple model and predict next movement
    """

    # Fetch data
    df = yf.download(symbol, period="6mo", interval="1d")

    df = compute_features(df)
    X, y = prepare_data(df)

    # Train model
    model = XGBClassifier(n_estimators=50, max_depth=3)   # can add random_state=42 to reduce randomness
    model.fit(X, y)

    # Latest data point
    latest = X.iloc[-1:].values

    prob = model.predict_proba(latest)[0][1]
    print("Latest features:", X.iloc[-1])
    return MLOutput(
        prob_up=float(prob),
        confidence=float(prob),
        prediction=int(prob > 0.5)
    )