from app.state import TradingState, MLOutput

state = TradingState()

state.ml_output = MLOutput(
    prob_up=0.7,
    confidence=0.65,
    prediction=1
)

print(state)