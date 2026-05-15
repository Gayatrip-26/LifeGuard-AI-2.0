from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List

from app.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate


def get_risk_trend(db: Session, user_id: int) -> dict:
    """Use the last 10 predictions; compare the two most recent scores for direction."""
    records: List[Prediction] = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .limit(10)
        .all()
    )
    if not records:
        return {
            "trend": "stable",
            "last_score": None,
            "previous_score": None,
        }
    last_score = records[0].risk_score
    if len(records) < 2:
        return {
            "trend": "stable",
            "last_score": last_score,
            "previous_score": None,
        }
    previous_score = records[1].risk_score
    if last_score > previous_score:
        trend = "increasing"
    elif last_score < previous_score:
        trend = "decreasing"
    else:
        trend = "stable"
    return {
        "trend": trend,
        "last_score": last_score,
        "previous_score": previous_score,
    }


def save_prediction(db: Session, data: PredictionCreate) -> Prediction:
    try:
        prediction = Prediction(**data.model_dump())

        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return prediction

    except Exception as e:
        db.rollback()
        raise e


def get_predictions_for_user(
    db: Session, user_id: int, limit: int = 10
) -> List[Prediction]:
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .limit(limit)
        .all()
    )


def get_dashboard_summary(db: Session, user_id: int) -> dict:
    total_records = (
        db.query(func.count(Prediction.id))
        .filter(Prediction.user_id == user_id)
        .scalar()
    ) or 0

    high_risk_count = (
        db.query(func.count(Prediction.id))
        .filter(
            Prediction.user_id == user_id,
            func.lower(func.trim(Prediction.risk_level)) == "high",
        )
        .scalar()
    ) or 0

    latest_prediction = (
        db.query(Prediction.risk_level)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    average_score = (
        db.query(func.avg(Prediction.risk_score))
        .filter(Prediction.user_id == user_id)
        .scalar()
    )

    trend = get_risk_trend(db, user_id)

    return {
        "total_records": int(total_records),
        "high_risk_count": int(high_risk_count),
        "latest_risk": latest_prediction[0] if latest_prediction else None,
        "average_score": round(float(average_score), 2) if average_score else 0.0,
        "risk_trend": trend,
    }
