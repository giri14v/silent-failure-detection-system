from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from collections import defaultdict

from app.storage.db import get_db_session
from app.storage.schemas import PredictionLog, CurrentWindowMetrics
from app.core.config import LOW_CONFIDENCE_THRESHOLD, CURRENT_WINDOW_MINUTES


def compute_current_window():
    db: Session = get_db_session()

    window_end = datetime.now(timezone.utc)
    window_start = window_end - timedelta(minutes=CURRENT_WINDOW_MINUTES)

    logs = (
        db.query(PredictionLog)
        .filter(PredictionLog.timestamp >= window_start)
        .filter(PredictionLog.timestamp <= window_end)
        .all()
    )

    if not logs:
        print("No prediction logs in current window.")
        return

    confidences = []
    low_conf_count = 0
    feature_anomalies = defaultdict(int)

    for log in logs:
        confidences.append(log.confidence_score)

        if log.confidence_score < LOW_CONFIDENCE_THRESHOLD:
            low_conf_count += 1

        for k, v in log.input_summary.items():
            if v is None:
                feature_anomalies[k] += 1

    metrics = CurrentWindowMetrics(
        window_start=window_start,
        window_end=window_end,
        prediction_count=len(logs),
        avg_confidence=sum(confidences) / len(confidences),
        low_confidence_rate=low_conf_count / len(logs),
        feature_anomalies=dict(feature_anomalies),
        unseen_categories=False
    )

    db.add(metrics)
    db.commit()
    db.close()

    print("Current window metrics stored.")


if __name__ == "__main__":
    compute_current_window()