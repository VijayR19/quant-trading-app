from datetime import datetime, timezone
import httpx
from app.core.config import settings

class MarketDataError(Exception):
    """Base exception class for market data related errors."""
    pass

def get_current_utc_time_isoformat() -> str:
    """Returns the current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds')

async def get_latest_market_price(symbol: str) -> dict:
    """
    Retrieves the latest market price for a given stock symbol.

    :param symbol: The stock symbol to retrieve the latest price for.
    :return: A dictionary containing the symbol, price, timestamp, and market data source.
    :raises MarketDataError: If the market data provider is not supported.
    """
    symbol = symbol.upper()

    market_provider = getattr(settings, "market_provider", "finnhub")

    if market_provider == "finnhub":
        return await _finnhub_quote(symbol)

    raise MarketDataError(f"Unsupported market data provider: {market_provider}")


async def _finnhub_quote(symbol: str) -> dict:
    """
    Retrieves the latest market price for a given stock symbol using Finnhub.

    :param symbol: The stock symbol to retrieve the latest price for.
    :return: A dictionary containing the symbol, price, timestamp, and market data source.
    :raises MarketDataError: If the Finnhub API key is not configured or no price data is available.
    """
    api_key = getattr(settings, "finnhub_api_key")
    if not api_key:
        raise MarketDataError("Finnhub API key is not configured")

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            "https://finnhub.io/api/v1/quote",
            params={"symbol": symbol, "token": api_key},
        )
        response.raise_for_status()
        data = response.json()

    price = data.get("c")
    if price is None or price == 0:
        raise MarketDataError(f"No price data available for symbol: {symbol}")

    return {
        "symbol": symbol,
        "price": price,
        "timestamp": get_current_utc_time_isoformat(),
        "source": "finnhub",
    }


async def get_recent_market_features(symbol: str) -> dict:
    """
    Fetch recent candles and compute simple features for the predictor.
    Features returned:
      - returns_30m
      - volatility
    """
    symbol = symbol.upper()

    provider = getattr(settings, "market_provider", "finnhub")
    if provider != "finnhub":
        raise MarketDataError(f"Unsupported market data provider: {provider}")

    candles = await _finnhub_candles_last_n_minutes(symbol=symbol, minutes=60, resolution="1")
    closes = candles["closes"]

    if len(closes) < 35:
        raise MarketDataError(f"Not enough candle data to compute features for {symbol}")

    # last 30 minutes return: (last / value 30m ago) - 1
    last = closes[-1]
    prev_30m = closes[-31]
    returns_30m = (last / prev_30m) - 1.0

    # simple volatility: std dev of 1-min returns over last 30 mins
    rets = []
    for i in range(len(closes) - 30, len(closes)):
        if i == 0:
            continue
        r = (closes[i] / closes[i - 1]) - 1.0
        rets.append(r)

    # compute std without numpy
    mean = sum(rets) / len(rets)
    var = sum((x - mean) ** 2 for x in rets) / max(len(rets) - 1, 1)
    volatility = var ** 0.5

    return {
        "symbol": symbol,
        "returns_30m": float(returns_30m),
        "volatility": float(volatility),
        "timestamp": get_current_utc_time_isoformat(),
        "source": "finnhub",
        "resolution": "1",
        "window_minutes": 60,
    }


async def _finnhub_candles_last_n_minutes(symbol: str, minutes: int, resolution: str = "1") -> dict:
    """
    Finnhub candles endpoint:
      https://finnhub.io/docs/api/stock-candles
    resolution: "1", "5", "15", "30", "60", "D", ...
    """
    api_key = getattr(settings, "finnhub_api_key")
    if not api_key:
        raise MarketDataError("Finnhub API key is not configured")

    # Finnhub expects UNIX seconds
    now = datetime.now(timezone.utc)
    to_ts = int(now.timestamp())
    from_ts = to_ts - (minutes * 60)

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(
            "https://finnhub.io/api/v1/stock/candle",
            params={
                "symbol": symbol,
                "resolution": resolution,
                "from": from_ts,
                "to": to_ts,
                "token": api_key,
            },
        )
        r.raise_for_status()
        data = r.json()

    # Finnhub returns {"s":"ok","c":[...], ...} or {"s":"no_data",...}
    if data.get("s") != "ok":
        raise MarketDataError(f"No candle data available for symbol: {symbol}")

    closes = data.get("c", [])
    if not closes:
        raise MarketDataError(f"No close prices available for symbol: {symbol}")

    return {
        "symbol": symbol,
        "closes": [float(x) for x in closes],
        "raw": data,
    }
