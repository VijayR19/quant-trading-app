from fastapi import APIRouter, Depends, HTTPException
from app.schemas import PredictRequest, PredictResponse
from app.deps import get_current_user_id

from app.services.predictor import predict_return_and_confidence
from app.services.market_data import get_recent_market_features

router = APIRouter(prefix="/api/predict", tags=["predict"])


@router.get("/predict", response_model=PredictResponse)
async def predict_endpoint(
    symbol: str,
    horizon_minutes: int = 30,
    user_id: int = Depends(get_current_user_id),
):
    """
    Predict the expected return and confidence over a time horizon.

    Parameters
    ----------
    symbol : str
        Stock symbol to predict for.
    horizon_minutes : int
        Prediction horizon in minutes.

    Returns
    -------
    PredictResponse
        (symbol, horizon_minutes, predicted_return, confidence)
    """
    features = await get_recent_market_features(symbol)
    pred, conf = await predict_return_and_confidence(features, horizon_minutes)

    return PredictResponse(
        symbol=symbol.upper(),
        horizon_minutes=horizon_minutes,
        predicted_return=pred,
        confidence=conf,
    )
