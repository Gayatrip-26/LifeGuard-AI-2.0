import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import ServiceOrUserContext, get_service_or_user
from app.db.session import get_db
from app.models.prediction import Prediction
from app.rag.rag_service import query_medical_info
from app.services.prediction_service import get_predictions_for_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])


class AIQueryRequest(BaseModel):
    query: str
    user_id: int | None = Field(
        default=None,
        description="Required for internal service calls; ignored for end users.",
    )


def _patient_history_insight(records: list[Prediction]) -> str | None:
    if not records:
        return None
    themes: list[str] = []
    risk_notes: list[str] = []
    for r in records:
        themes.extend(r.issues or [])
        rl = (r.risk_level or "").strip().upper()
        if rl == "HIGH":
            risk_notes.append("high risk episode")
        elif rl == "MEDIUM":
            risk_notes.append("moderate risk episode")

    uniq_issues = sorted({t.lower() for t in themes})
    stress = any("stress" in i for i in uniq_issues)
    sleep = any("sleep" in i for i in uniq_issues)

    parts: list[str] = []
    if stress and sleep:
        parts.append("repeated high stress and low sleep patterns")
    elif stress:
        parts.append("recurring stress-related findings")
    elif sleep:
        parts.append("ongoing sleep-related concerns")

    if parts:
        return f"Patient history shows {' and '.join(parts)} across recent assessments."

    if uniq_issues:
        return (
            "Patient history highlights recurring themes: "
            f"{', '.join(uniq_issues)}."
        )

    if risk_notes:
        return (
            "Patient history includes "
            f"{', '.join(risk_notes)} in the latest stored assessments."
        )

    return (
        "Patient history shows recent assessments; continue monitoring trends over time."
    )


def _resolve_ai_user_id(payload: AIQueryRequest, ctx: ServiceOrUserContext) -> int:
    if ctx.is_service:
        if payload.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id is required for internal AI requests.",
            )
        return payload.user_id
    if ctx.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )
    if payload.user_id is not None and payload.user_id != ctx.user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot query history for another user.",
        )
    return ctx.user.id


@router.post("/query")
def query_ai(
    payload: AIQueryRequest,
    db: Session = Depends(get_db),
    ctx: ServiceOrUserContext = Depends(get_service_or_user),
) -> dict:
    try:
        if not settings.ai_enabled:
            return {
                "answer": "AI assistance is currently disabled.",
                "recommended_actions": [],
            }

        user_id = _resolve_ai_user_id(payload, ctx)
        recent = get_predictions_for_user(db, user_id, limit=3)
        history = _patient_history_insight(recent)

        return query_medical_info(payload.query, patient_history_summary=history)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("AI query failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to complete AI query. Please try again later.",
        ) from exc
