# app/routers/trade.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user_id
from app.schemas import TradeCreate, TradeRead
from app.models import Trade
from app.services.market_data import get_latest_price

router = APIRouter(prefix="/api/trade", tags=["trade"])

@router.post("", response_model=TradeRead)
def create_trade(trade_data: TradeCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)) -> TradeRead:
    """
    Create a new trade.

    Args:
        trade_data (TradeCreate): The trade data.
        db (Session): The database session.
        user_id (int): The ID of the user placing the trade.

    Returns:
        TradeRead: The created trade.
    """
    latest_price = get_latest_price(trade_data.symbol)["price"]

    trade = Trade(
        user_id=user_id,
        symbol=trade_data.symbol.upper(),
        side=trade_data.side,
        quantity=trade_data.quantity,
        price=latest_price,
        status="FILLED",  # paper fill at current price
    )
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

@router.get("/my", response_model=list[TradeRead])
def get_my_trades(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)) -> list[TradeRead]:
    """
    Retrieve all trades placed by the current user.

    Args:
        db (Session): The database session.
        current_user_id (int): The ID of the current user.

    Returns:
        list[TradeRead]: A list of trades placed by the current user.
    """
    trades = db.query(Trade).filter(Trade.user_id == current_user_id).order_by(Trade.id.desc()).all()
    return trades
