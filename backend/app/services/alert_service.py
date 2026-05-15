import logging

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert import AlertCreate

logger = logging.getLogger(__name__)


def create_alert(db: Session, data: AlertCreate) -> Alert:
    alert = Alert(
        user_id=data.user_id,
        patient_id=data.patient_id,
        message=data.message,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    logger.info("Alert created id=%s user_id=%s", alert.id, alert.user_id)
    return alert


def get_alerts_for_user(db: Session, user_id: int, limit: int = 100) -> list[Alert]:
    return (
        db.query(Alert)
        .filter(Alert.user_id == user_id)
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .all()
    )
