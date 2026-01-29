# monitoring/force_degraded_window.py

from datetime import datetime, timedelta, timezone

from app.storage.db import get_db_session
from app.storage.schemas import CurrentWindowMetrics


def insert_forced_degraded_window():
    db = get_db_session()

    now = datetime.now(timezone.utc)

    forced = CurrentWindowMetrics(
        window_start=now - timedelta(minutes=5),
        window_end=now,
        prediction_count=100,
        avg_confidence=0.35,          # VERY LOW
        low_confidence_rate=0.82,     # VERY HIGH
        feature_anomalies={},
        unseen_categories=False,
    )

    db.add(forced)
    db.commit()
    db.close()

    print("Forced degraded window inserted.")


if __name__ == "__main__":
    insert_forced_degraded_window()