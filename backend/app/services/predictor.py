from typing import Mapping, Any, Tuple


def predict_return_and_confidence(
    features: Mapping[str, float],
    horizon_minutes: int,
) -> Tuple[float, float]:
    """
    Predict the expected return and confidence over a time horizon.

    Parameters
    ----------
    features : dict
        Feature dictionary derived from market data.
        Expected keys (optional):
        - returns_30m
        - volatility
    horizon_minutes : int
        Prediction horizon in minutes.

    Returns
    -------
    tuple(float, float)
        (predicted_return, confidence)
    """

    returns_30m = features.get("returns_30m", 0.0)
    volatility = features.get("volatility", 0.3)

    predicted_return = min(max(returns_30m * 0.8, -0.05), 0.05)
    confidence = min(max(0.85 - volatility * 0.5, 0.50), 0.85)

    return predicted_return, confidence
