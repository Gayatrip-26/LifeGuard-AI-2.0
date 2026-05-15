import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.deps import ServiceOrUserContext, ensure_user_id_matches, get_service_or_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.prediction import (
    DashboardSummaryResponse,
    PredictionCreate,
    PredictionResponse,
    RiskTrendBlock,
)
from app.services.prediction_service import (
    get_dashboard_summary,
    get_predictions_for_user,
    save_prediction,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/prediction", tags=["prediction"])
dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.post("/save", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def save_prediction_endpoint(
    payload: PredictionCreate,
    db: Session = Depends(get_db),
    ctx: ServiceOrUserContext = Depends(get_service_or_user),
):
    try:
        ensure_user_id_matches(ctx, payload.user_id)
        return save_prediction(db, payload)
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Failed to save prediction: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save prediction.",
        ) from exc
    except Exception as exc:
        db.rollback()
        logger.exception("Unexpected error saving prediction: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while saving the prediction.",
        ) from exc


@router.get("", response_model=list[PredictionResponse])
def get_prediction_history_endpoint(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_predictions_for_user(db, current_user.id, limit=limit)
    except SQLAlchemyError as exc:
        logger.exception("Failed to load predictions: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load prediction history.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error loading predictions: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load prediction history.",
        ) from exc


@dashboard_router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        summary = get_dashboard_summary(db, current_user.id)
        trend = summary.get("risk_trend") or {}
        payload = {
            **{k: v for k, v in summary.items() if k != "risk_trend"},
            "risk_trend": RiskTrendBlock(**trend),
        }
        return DashboardSummaryResponse(**payload)
    except SQLAlchemyError as exc:
        logger.exception("Failed to load dashboard summary: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load dashboard summary.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error loading dashboard summary: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load dashboard summary.",
        ) from exc
