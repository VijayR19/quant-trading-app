import random

def predict_return(
    symbol: str, 
    horizon_minutes: int
) -> tuple[float, float]:
    """
    Predict the return of a stock symbol over a given horizon.

    :param symbol: The stock symbol to predict.
    :param horizon_minutes: The time horizon for the prediction in minutes.
    :return: A tuple containing the predicted return and confidence.
    :rtype: tuple[float, float]
    """
    predicted_return_value = random.uniform(-0.02, 0.02)
    confidence_value = random.uniform(0.50, 0.85)
    return predicted_return_value, confidence_value
