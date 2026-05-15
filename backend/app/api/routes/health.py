import logging

from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check() -> dict:
    try:
        return {"status": "ok", "service": "backend"}
    except Exception as exc:
        logger.exception("Health check failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed.",
        ) from exc
