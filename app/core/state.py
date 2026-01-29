from datetime import datetime
from sqlalchemy.orm import Session

from app.core.config import STATE_NORMAL
from app.storage.schemas import SystemState
from app.storage.db import get_db_session


def get_current_state(db: Session = None) -> SystemState:
    """Return the latest system state from DB. If none exists, initialize NORMAL."""
    close_after = False
    if db is None:
        db = get_db_session()
        close_after = True

    state = db.query(SystemState).order_by(SystemState.last_updated.desc()).first()

    if not state:
        state = SystemState(
            current_state=STATE_NORMAL,
            last_updated=datetime.utcnow(),
            reason="System initialized"
        )
        db.add(state)
        db.commit()
        db.refresh(state)

    if close_after:
        db.close()

    return state


def set_system_state(new_state: str, reason: str, db: Session = None):
    """Persist a new system state."""
    close_after = False
    if db is None:
        db = get_db_session()
        close_after = True

    state = SystemState(
        current_state=new_state,
        last_updated=datetime.utcnow(),
        reason=reason
    )
    db.add(state)
    db.commit()

    if close_after:
        db.close()

    return state