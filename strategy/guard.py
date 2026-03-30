from app.state import (
    MLOutput,
    MarketAnalysis,
    SentimentOutput,
    RiskAnalysis,
    DecisionOutput,
    FinalSignal
)


def strategy_guard(
    ml_output: MLOutput,
    market: MarketAnalysis,
    sentiment: SentimentOutput,
    risk: RiskAnalysis,
    decision: DecisionOutput
) -> FinalSignal:
    """
    Final deterministic validation before trade execution
    """

    prob = ml_output.prob_up
    trend = market.trend
    sentiment_score = sentiment.score
    risk_level = risk.risk_level
    llm_action = decision.action

    # =========================
    # RULE 1: Risk Filter (HARD STOP)
    # =========================
    if risk_level == "high":
        return FinalSignal(
            action="HOLD",
            confidence=0.9,
            reason="High risk - trade blocked"
        )

    # =========================
    # RULE 2: Strong BUY Conditions
    # =========================
    if (
        prob > 0.65 and
        trend == "bullish" and
        sentiment_score > 0.1 and
        llm_action == "BUY"
    ):
        return FinalSignal(
            action="BUY",
            confidence=round(prob, 2),
            reason="All signals aligned (ML + trend + sentiment)"
        )

    # =========================
    # RULE 3: Strong SELL Conditions
    # =========================
    if (
        prob < 0.4 and
        trend == "bearish" and
        sentiment_score < -0.1 and
        llm_action == "SELL"
    ):
        return FinalSignal(
            action="SELL",
            confidence=round(1 - prob, 2),
            reason="Bearish alignment across signals"
        )

    # =========================
    # RULE 4: Conflict → HOLD
    # =========================
    return FinalSignal(
        action="HOLD",
        confidence=0.5,
        reason="Signals not strongly aligned"
    )