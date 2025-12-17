from fastapi import APIRouter, Depends
from app.services.market_data import get_latest_market_price
from app.deps import get_current_user_id



router = APIRouter(prefix="/api/market", tags=["market"])

@router.get("/price/{symbol}")
async def get_latest_market_price(symbol: str, user_id: int = Depends(get_current_user_id)):
    """
    Retrieves the latest market price for a given stock symbol.

    Args:
        symbol (str): The stock symbol to retrieve the latest price for.
        user_id (int): The ID of the user making the request.

    Returns:
        dict: A dictionary containing the symbol, price, timestamp, and market data source.
    """
    quote = await get_latest_market_price(symbol)
    return {
        quote["symbol"]: quote["price"]
    }
