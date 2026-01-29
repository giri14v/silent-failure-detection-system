from app.storage.schemas import Incident, BaselineMetrics, CurrentWindowMetrics


def build_incident_payload(
    incident: Incident,
    baseline: BaselineMetrics,
    current: CurrentWindowMetrics,
):
    """
    Deterministic, structured payload for LLM.
    No interpretation. No decisions.
    """

    return {
        "incident_id": incident.incident_id,
        "severity": incident.severity,
        "decision_reason": incident.decision_reason,
        "trigger_signals": incident.trigger_signals,
        "baseline_metrics": {
            "avg_confidence": baseline.avg_confidence,
            "low_confidence_rate": baseline.low_confidence_rate,
        },
        "current_window_metrics": {
            "avg_confidence": current.avg_confidence,
            "low_confidence_rate": current.low_confidence_rate,
            "prediction_count": current.prediction_count,
        },
        "fallback_activated": incident.fallback_activated,
    }