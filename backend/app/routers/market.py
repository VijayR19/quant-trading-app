# app/routers/market.py
from fastapi import APIRouter, Depends
from app.deps import get_current_user_id
from app.services.market_data import get_latest_price, get_recent_features

router = APIRouter(prefix="/api/market", tags=["market"])

@router.get("/price", response_model=dict[str, float])
def get_latest_market_price(
    symbol: str, user_id: int = Depends(get_current_user_id)
) -> dict[str, float]:
    """
    Returns the latest market price for a given stock symbol.

    :param symbol: The stock symbol to retrieve the latest price for.
    :param user_id: The ID of the user making the request.
    :return: A dictionary containing the symbol and the latest price.
    """
    return {symbol.upper(): get_latest_price(symbol)}

@router.get("/features", response_model=dict[str, dict])
def get_recent_market_features(
    symbol: str, user_id: int = Depends(get_current_user_id)
) -> dict[str, dict]:
    """
    Returns the most recent market features for a given stock symbol.

    :param symbol: The stock symbol to retrieve the most recent features for.
    :param user_id: The ID of the user making the request.
    :return: A dictionary containing the symbol and the most recent features.
    """
    return {
        "symbol": symbol.upper(),
        "features": get_recent_features(symbol)
    }
