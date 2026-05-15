import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.health import HealthDataCreate, HealthDataResponse
from app.services.health_service import add_health_data, get_health_history
from app.services.user_service import get_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health-data"])


@router.post("", response_model=HealthDataResponse, status_code=status.HTTP_201_CREATED)
def add_health_data_endpoint(
    payload: HealthDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HealthDataResponse:
    try:
        if payload.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only submit health data for your own account.",
            )
        user = get_user(db, payload.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return add_health_data(db, payload)
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Failed to add health data: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save health data.",
        ) from exc
    except Exception as exc:
        db.rollback()
        logger.exception("Unexpected error adding health data: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from exc


@router.get("/{user_id}", response_model=list[HealthDataResponse])
def get_health_history_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[HealthDataResponse]:
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own health history.",
            )
        return get_health_history(db, user_id)
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        logger.exception("Failed to load health history: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load health history.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error loading health history: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load health history.",
        ) from exc
