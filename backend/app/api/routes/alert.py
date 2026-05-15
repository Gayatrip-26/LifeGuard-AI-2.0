import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.deps import require_internal_service
from app.db.session import get_db
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertResponse
from app.services.alert_service import create_alert, get_alerts_for_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alert", tags=["alerts"])


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert_endpoint(
    payload: AlertCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_internal_service),
):
    try:
        alert = create_alert(db, payload)
        return AlertResponse.model_validate(alert)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Failed to create alert: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not store alert. Please try again.",
        ) from exc
    except Exception as exc:
        db.rollback()
        logger.exception("Unexpected error creating alert: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from exc


@router.get("", response_model=list[AlertResponse])
def list_alerts_for_current_user(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        rows = get_alerts_for_user(db, current_user.id, limit=limit)
        return [AlertResponse.model_validate(r) for r in rows]
    except SQLAlchemyError as exc:
        logger.exception("Failed to list alerts: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load alerts.",
        ) from exc
