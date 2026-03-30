from app.state import TechnicalIndicators, MarketAnalysis
from agents.prompts import MARKET_AGENT_PROMPT
from agents.utils import call_llm
import json


def market_agent(technicals: TechnicalIndicators) -> MarketAnalysis:
    """
    Analyze market indicators and return structured market analysis
    """

    # Prepare input for LLM
    input_data = {
        "rsi": technicals.rsi,
        "ema20": technicals.ema20,
        "ema50": technicals.ema50,
        "macd": technicals.macd,
        "volume": technicals.volume,
    }

    # Create prompt
    prompt = MARKET_AGENT_PROMPT.format(data=json.dumps(input_data, indent=2))

    # Call LLM
    response = call_llm(prompt)

    try:
        parsed = json.loads(response)
        return MarketAnalysis(**parsed)

    except Exception as e:
        raise ValueError(f"Market Agent failed to parse response: {e}")