from collections import defaultdict
from sqlalchemy.orm import Session

from app.models import Trade
from app.services.market_data import get_latest_market_price, MarketDataError


# -------------------------
# Trade execution (paper)
# -------------------------

async def execute_trade(
    db: Session,
    user_id: int,
    symbol: str,
    side: str,
    quantity: int,
) -> Trade:
    """
    Execute a paper trade at current market price.
    """
    quote = await get_latest_market_price(symbol)

    trade = Trade(
        user_id=user_id,
        symbol=symbol.upper(),
        side=side,
        quantity=quantity,
        price=quote["price"],
        status="FILLED",
    )

    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade


# -------------------------
# Positions
# -------------------------

def get_positions(db: Session, user_id: int) -> dict[str, int]:
    trades = db.query(Trade).filter(Trade.user_id == user_id).all()

    positions = defaultdict(int)
    for t in trades:
        sign = 1 if t.side == "BUY" else -1
        positions[t.symbol] += sign * t.quantity

    return dict(positions)


# -------------------------
# PnL
# -------------------------

async def get_pnl(db: Session, user_id: int) -> list[dict]:
    trades = db.query(Trade).filter(Trade.user_id == user_id).all()

    qty = defaultdict(int)
    cost = defaultdict(float)

    for t in trades:
        px = float(t.price)
        if t.side == "BUY":
            qty[t.symbol] += t.quantity
            cost[t.symbol] += t.quantity * px
        else:
            qty[t.symbol] -= t.quantity
            cost[t.symbol] -= t.quantity * px

    results = []
    for symbol, quantity in qty.items():
        if quantity == 0:
            continue

        avg_entry = cost[symbol] / quantity

        quote = await get_latest_market_price(symbol)
        last_price = float(quote["price"])

        unrealized = (last_price - avg_entry) * quantity

        results.append(
            {
                "symbol": symbol,
                "quantity": quantity,
                "avg_entry": avg_entry,
                "last_price": last_price,
                "unrealized_pnl": unrealized,
            }
        )

    return results
