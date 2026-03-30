from pydantic import BaseModel, Field
from typing import List, Optional


# =========================
# ML OUTPUT
# =========================
class MLOutput(BaseModel):
    prob_up: float = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0, le=1)
    prediction: int  # 1 = up, 0 = down


# =========================
# MARKET DATA (basic)
# =========================
class MarketData(BaseModel):
    symbol: str
    close: float
    volume: float


# =========================
# FEATURES (technical indicators)
# =========================
class TechnicalIndicators(BaseModel):
    rsi: float
    ema20: float
    ema50: float
    macd: float
    volume: float


# =========================
# NEWS DATA
# =========================
class NewsData(BaseModel):
    headlines: List[str]


# =========================
# SENTIMENT OUTPUT
# =========================
class SentimentOutput(BaseModel):
    overall_sentiment: str  # positive | negative | neutral
    score: float = Field(..., ge=-1, le=1)
    confidence: float = Field(..., ge=0, le=1)
    summary: str


# =========================
# MARKET AGENT OUTPUT
# =========================
class MarketAnalysis(BaseModel):
    trend: str              # bullish | bearish | sideways
    strength: float = Field(..., ge=0, le=1)
    momentum: str           # strong | weak
    reason: str


# =========================
# RISK AGENT OUTPUT
# =========================
class RiskAnalysis(BaseModel):
    risk_level: str         # low | medium | high
    position_size: float    # e.g. 0.02 (2%)
    stop_loss: float        # %
    take_profit: float      # %
    warning: str


# =========================
# DECISION AGENT OUTPUT
# =========================
class DecisionOutput(BaseModel):
    action: str             # BUY | SELL | HOLD
    confidence: float = Field(..., ge=0, le=1)
    reason: str


# =========================
# FINAL SIGNAL (after guard)
# =========================
class FinalSignal(BaseModel):
    action: str             # BUY | SELL | HOLD
    confidence: float
    reason: str


# =========================
# GLOBAL STATE
# =========================
class TradingState(BaseModel):
    # Raw inputs
    market_data: Optional[MarketData] = None
    technicals: Optional[TechnicalIndicators] = None
    news: Optional[NewsData] = None

    # ML + agents
    ml_output: Optional[MLOutput] = None
    sentiment: Optional[SentimentOutput] = None
    market_analysis: Optional[MarketAnalysis] = None
    risk_analysis: Optional[RiskAnalysis] = None
    decision: Optional[DecisionOutput] = None

    # Final output
    final_signal: Optional[FinalSignal] = None