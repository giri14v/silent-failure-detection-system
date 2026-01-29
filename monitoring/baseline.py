# monitoring/baseline.py
from collections import defaultdict
from sqlalchemy.orm import Session

from app.storage.db import get_db_session
from app.storage.schemas import PredictionLog, BaselineMetrics
from app.core.config import LOW_CONFIDENCE_THRESHOLD, BASELINE_SAMPLE_SIZE


def compute_baseline():
    db: Session = get_db_session()

    logs = (
        db.query(PredictionLog)
        .order_by(PredictionLog.timestamp.asc())
        .limit(BASELINE_SAMPLE_SIZE)
        .all()
    )

    if not logs:
        print("No prediction logs available for baseline")
        return

    confidences = []
    low_conf_count = 0

    feature_ranges = defaultdict(lambda: {"min": float("inf"), "max": float("-inf")})
    missing_counts = defaultdict(int)
    total = len(logs)

    for log in logs:
        confidences.append(log.confidence_score)

        if log.confidence_score < LOW_CONFIDENCE_THRESHOLD:
            low_conf_count += 1

        for k, v in log.input_summary.items():
            if v is None:
                missing_counts[k] += 1
            else:
                feature_ranges[k]["min"] = min(feature_ranges[k]["min"], v)
                feature_ranges[k]["max"] = max(feature_ranges[k]["max"], v)

    baseline = BaselineMetrics(
        baseline_id="default",
        sample_size=total,
        avg_confidence=sum(confidences) / total,
        low_confidence_rate=low_conf_count / total,
        feature_ranges=dict(feature_ranges),
        missing_value_rates={k: v / total for k, v in missing_counts.items()},
        category_frequencies={}
    )

    db.merge(baseline)
    db.commit()
    db.close()

    print("Baseline computed and stored.")

if __name__ == "__main__":
    compute_baseline()