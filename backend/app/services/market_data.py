from datetime import datetime, timezone
import random

def get_lastest_price(symbol: str) -> dict:
    """
    Returns a dictionary containing the latest price for a given stock symbol.

    Parameters:
    symbol (str): The stock symbol to retrieve the latest price for.

    Returns:
    dict: A dictionary containing the symbol, price, timestamp, and source of the latest price.
    """
    symbol = symbol.upper()
    return {
        "symbol": symbol,
        "price": round(random.uniform(50, 250), 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "stub"
    }

def get_recent_features(symbol: str) -> dict:
    # Later: compute from bars (returns, vol, RSI, etc.)
    """
    Returns a dictionary containing the most recent features for a given stock symbol.

    Parameters:
    symbol (str): The stock symbol to retrieve the most recent features for.

    Returns:
    dict: A dictionary containing the most recent features for the given stock symbol.
    Features currently include:
    - return_5m: the return over the past 5 minutes
    - returns_30m: the return over the past 30 minutes
    - volatility: the volatility of the stock over the past 30 minutes
    - volume_z: the volume of the stock over the past 30 minutes, normalized by the mean and standard deviation of the past 30 minutes
    """
    symbol = symbol.upper()
    return {
        "return_5m": random.uniform(-0.01, 0.01),
        "returns_30m": random.uniform(-0.03, 0.03),
        "volatility": random.uniform(0.1, 0.6),
        "volume_z": random.uniform(-2, 2),
    }
    