import uuid
from sqlalchemy.orm import Session

from app.storage.db import get_db_session
from app.storage.schemas import (
    BaselineMetrics,
    CurrentWindowMetrics,
    Incident,
)
from app.core.state import get_current_state, set_system_state
from monitoring.deviation import evaluate_deviation


RECOVERY_REQUIRED_RUNS = 2  # deterministic, explainable


def run_monitoring():
    db: Session = get_db_session()

    baseline = db.query(BaselineMetrics).filter_by(baseline_id="default").first()
    current = (
        db.query(CurrentWindowMetrics)
        .order_by(CurrentWindowMetrics.window_end.desc())
        .first()
    )

    if not baseline or not current:
        print("Baseline or current window missing")
        return

    new_state, signals, reason = evaluate_deviation(baseline, current)
    current_state = get_current_state(db)

    # ----------------------------
    # CASE 1: Degradation detected
    # ----------------------------
    if new_state != current_state.current_state and new_state != "NORMAL":
        set_system_state(new_state, reason, db)

        incident = Incident(
            incident_id=str(uuid.uuid4()),
            severity=new_state,
            trigger_signals=signals,
            decision_reason=reason,
            fallback_activated=(new_state == "DEGRADED"),
            resolved=False,
        )
        db.add(incident)
        db.commit()

        print(f"State changed to {new_state}. Incident created.")

    # ----------------------------
    # CASE 2: Recovery detection
    # ----------------------------
    elif current_state.current_state == "DEGRADED" and new_state == "NORMAL":
        open_incidents = (
            db.query(Incident)
            .filter_by(resolved=False)
            .all()
        )

        if len(open_incidents) >= RECOVERY_REQUIRED_RUNS:
            set_system_state("NORMAL", "Recovered after sustained stability", db)

            for incident in open_incidents:
                incident.resolved = True

            db.commit()
            print("System recovered. Fallback disabled. Incidents resolved.")
        else:
            print("Recovery signal detected but not yet stable.")

    else:
        print("No state change.")

    db.close()


if __name__ == "__main__":
    run_monitoring()