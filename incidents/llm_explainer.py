# incidents/llm_explainer.py

from datetime import datetime, timezone
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from app.storage.db import get_db_session
from app.storage.schemas import LLMExplanation

# ---------------------------------------------------------
# Load BART once at startup (CPU, observer-only)
# ---------------------------------------------------------
MODEL_NAME = "facebook/bart-large-cnn"

_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
_model.eval()  # inference only


def _format_incident(payload: dict) -> str:
    return (
        "During routine prediction monitoring, the system detected a deviation.\n"
        f"The incident was classified as {payload.get('severity')} severity.\n"
        f"The primary observation was that model confidence dropped below its baseline.\n"
        f"Historically, average confidence was {payload.get('baseline_metrics', {}).get('avg_confidence')}.\n"
        f"In the current window, average confidence declined to "
        f"{payload.get('current_window_metrics', {}).get('avg_confidence')} "
        f"across {payload.get('current_window_metrics', {}).get('prediction_count')} predictions.\n"
        f"Observed signals included: {payload.get('trigger_signals')}.\n"
        f"No fallback mechanism was activated."
    )


def explain_incident(payload: dict):
    """
    Observer-only LLM explainer.
    NEVER affects system behavior.
    """

    try:
        text = _format_incident(payload)

        inputs = _tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )

        with torch.no_grad():
            summary_ids = _model.generate(
                inputs["input_ids"],
                max_length=80,
                min_length=30,
                do_sample=False,
            )

        narrative = _tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True
        )

        metrics_summary = (
            f" Baseline avg confidence: "
            f"{payload.get('baseline_metrics', {}).get('avg_confidence')}. "
            f"Current avg confidence: "
            f"{payload.get('current_window_metrics', {}).get('avg_confidence')} "
            f"over {payload.get('current_window_metrics', {}).get('prediction_count')} predictions. "
            f"Trigger signals: {payload.get('trigger_signals')}."
        )

        summary_text = narrative.rstrip(".") + "." + metrics_summary

        db = get_db_session()
        db.add(
            LLMExplanation(
                incident_id=payload["incident_id"],
                generated_at=datetime.now(timezone.utc),
                summary=summary_text,
                recommendations="",  # observer-only by design
                llm_model="facebook/bart-large-cnn (local)",
            )
        )
        db.commit()
        db.close()

        print("LLM explanation stored (local BART).")

    except Exception as e:
        # Observer-only guarantee
        print(f"LLM explainer failed safely: {e}")