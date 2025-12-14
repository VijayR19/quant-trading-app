from fastapi import APIRouter, Depends, HTTPException
from app.schemas import PredictRequest, PredictResponse
from app.deps import get_current_user_id
from app.services.predictor import predict_return

router = APIRouter(prefix="/api/predict", tags=["predict"])

@router.post("/", response_model=PredictResponse)
def predict(
    payload: PredictRequest,
    user_id: int = Depends(get_current_user_id)
) -> PredictResponse:
    """
    Predict the return of a stock symbol over a given horizon.

    :param payload: The prediction request containing the stock symbol and horizon in minutes.
    :param user_id: The ID of the user making the request.
    :return: A prediction response containing the predicted return and confidence.
    :rtype: PredictResponse
    """
    pred, conf = predict_return(payload.symbol.upper(), payload.horizon_minutes)
    return PredictResponse(
        symbol=payload.symbol.upper(),
        horizon_minutes=payload.horizon_minutes,
        predicted_return=pred,
        confidence=conf,
    )
    