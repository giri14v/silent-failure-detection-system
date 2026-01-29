from app.core.config import (
    MAX_CONFIDENCE_DROP,
    MAX_LOW_CONFIDENCE_INCREASE,
    STATE_NORMAL,
    STATE_WARNING,
    STATE_DEGRADED,
)


def evaluate_deviation(baseline, current):
    """
    Returns: (state, trigger_signals, reason)
    """

    signals = {}

    # Confidence drift
    confidence_drop = baseline.avg_confidence - current.avg_confidence
    signals["confidence_drop"] = confidence_drop

    # Low-confidence spike
    low_conf_increase = current.low_confidence_rate - baseline.low_confidence_rate
    signals["low_confidence_increase"] = low_conf_increase

    critical = False
    warning = False

    if confidence_drop > MAX_CONFIDENCE_DROP:
        warning = True
    if low_conf_increase > MAX_LOW_CONFIDENCE_INCREASE:
        warning = True

    if confidence_drop > MAX_CONFIDENCE_DROP * 2:
        critical = True
    if low_conf_increase > MAX_LOW_CONFIDENCE_INCREASE * 2:
        critical = True

    if critical:
        return STATE_DEGRADED, signals, "Severe sustained confidence degradation"

    if warning:
        return STATE_WARNING, signals, "Moderate deviation from baseline"

    return STATE_NORMAL, signals, "Within normal range"