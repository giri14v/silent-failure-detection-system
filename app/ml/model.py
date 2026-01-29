import pickle
from pathlib import Path

from app.core.config import MODEL_VERSION

MODEL_PATH = Path("data/model.pkl")

_model = None


def load_model():
    global _model
    if _model is None:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def predict(features: list):
    model = load_model()

    raw_pred = model.predict([features])[0]
    prediction = int(raw_pred)   # convert numpy → python

    if hasattr(model, "predict_proba"):
        raw_conf = max(model.predict_proba([features])[0])
        confidence = float(raw_conf)   # convert numpy → python
    else:
        confidence = 1.0

    return prediction, confidence, MODEL_VERSION