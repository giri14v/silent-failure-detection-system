from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.ml.validation import validate_input, ValidationError
from app.ml.model import predict as ml_predict
from app.core.state import get_current_state
from app.fallback.rules import apply_fallback
from app.storage.db import get_db_session
from app.storage.schemas import PredictionLog
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger("predict")


@router.post("/predict")
def predict(payload: dict):
    db = get_db_session()

    try:
        features = validate_input(payload)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    system_state = get_current_state(db)

    fallback_used = False

    if system_state.current_state == "DEGRADED":
        prediction, confidence = apply_fallback(features)
        fallback_used = True
        model_version = "fallback"
    else:
        prediction, confidence, model_version = ml_predict(features)

    log = PredictionLog(
        timestamp=datetime.utcnow(),
        model_version=model_version,
        system_state=system_state.current_state,
        input_summary=payload,
        prediction=str(prediction),
        confidence_score=confidence,
        fallback_used=fallback_used,
    )

    db.add(log)
    db.commit()

    logger.info(
        "prediction_made",
        extra={"extra_data": {
            "model_version": model_version,
            "state": system_state.current_state,
            "confidence": confidence,
            "fallback": fallback_used
        }}
    )

    return {
        "prediction": prediction,
        "confidence": confidence,
        "system_state": system_state.current_state,
        "fallback_used": fallback_used
    }