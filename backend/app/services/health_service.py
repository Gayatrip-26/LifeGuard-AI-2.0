from sqlalchemy.orm import Session

from app.core.redis import set_cache
from app.models.health_data import HealthData
from app.schemas.health import HealthDataCreate


def add_health_data(db: Session, payload: HealthDataCreate) -> HealthData:
    health_data = HealthData(
        user_id=payload.user_id,
        heart_rate=payload.heart_rate,
        temperature=payload.temperature,
        stress_level=payload.stress_level,
        sleep_hours=payload.sleep_hours,
        timestamp=payload.timestamp,
    )
    db.add(health_data)
    db.commit()
    db.refresh(health_data)

    cache_key = f"user:{payload.user_id}:latest_health"
    set_cache(
        cache_key,
        {
            "id": health_data.id,
            "user_id": health_data.user_id,
            "heart_rate": health_data.heart_rate,
            "temperature": health_data.temperature,
            "stress_level": health_data.stress_level,
            "sleep_hours": health_data.sleep_hours,
            "timestamp": health_data.timestamp.isoformat(),
        },
    )

    return health_data


def get_health_history(db: Session, user_id: int) -> list[HealthData]:
    return (
        db.query(HealthData)
        .filter(HealthData.user_id == user_id)
        .order_by(HealthData.timestamp.desc())
        .all()
    )
