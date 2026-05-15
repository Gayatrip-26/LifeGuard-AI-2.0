import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)) -> UserResponse:
    try:
        return UserResponse.model_validate(current_user)
    except Exception as exc:
        logger.exception("Failed to serialize user profile: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load profile.",
        ) from exc
