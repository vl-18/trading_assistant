from app.state import (
    MLOutput,
    MarketAnalysis,
    SentimentOutput,
    RiskAnalysis,
    DecisionOutput
)
from agents.utils import call_llm
import json
import re


DECISION_PROMPT = """
You are an expert trading decision system.

You are given multiple signals:

ML Prediction:
{ml_output}

Market Analysis:
{market_analysis}

News Sentiment:
{sentiment}

Risk Analysis:
{risk_analysis}

Based on ALL inputs, decide:
- BUY
- SELL
- HOLD

Rules:
- If signals conflict → prefer HOLD
- High risk → avoid BUY
- Strong bullish + positive sentiment + good ML → BUY
- Strong bearish + negative sentiment → SELL

Return STRICT JSON:
{{
  "action": "BUY" | "SELL" | "HOLD",
  "confidence": float (0 to 1),
  "reason": "short explanation"
}}

IMPORTANT:
- Output ONLY JSON
- No extra text
"""


def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Invalid JSON response")


def decision_agent(
    ml_output: MLOutput,
    market_analysis: MarketAnalysis,
    sentiment: SentimentOutput,
    risk_analysis: RiskAnalysis
) -> DecisionOutput:

    prompt = DECISION_PROMPT.format(
        ml_output=ml_output.model_dump(),
        market_analysis=market_analysis.model_dump(),
        sentiment=sentiment.model_dump(),
        risk_analysis=risk_analysis.model_dump()
    )

    response = call_llm(prompt)

    try:
        parsed = extract_json(response)
        return DecisionOutput(**parsed)

    except Exception as e:
        raise ValueError(f"Decision Agent failed: {e}\nRaw response: {response}")