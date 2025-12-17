from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user_id
from app.schemas import TradeCreate, TradeRead, PositionRead, PnLRead
from app.services.trade_service import (
    execute_trade,
    get_positions,
    get_pnl,
)
from app.services.market_data import MarketDataError

router = APIRouter(prefix="/api/trade", tags=["trade"])


@router.post("", response_model=TradeRead)
async def place_trade(
    payload: TradeCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    try:
        trade = await execute_trade(
            db=db,
            user_id=user_id,
            symbol=payload.symbol,
            side=payload.side,
            quantity=payload.quantity,
        )
        return trade
    except MarketDataError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/positions", response_model=list[PositionRead])
def positions(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    positions = get_positions(db, user_id)
    return [
        PositionRead(symbol=s, quantity=q)
        for s, q in positions.items()
        if q != 0
    ]


@router.get("/pnl", response_model=list[PnLRead])
async def pnl(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await get_pnl(db, user_id)
