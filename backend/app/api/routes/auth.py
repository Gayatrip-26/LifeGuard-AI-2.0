import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.security import verify_password
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.user_service import create_user_with_password, get_user_by_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserResponse:
    try:
        if get_user_by_email(db, payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )
        user = create_user_with_password(db, payload.email, payload.password)
        return UserResponse.model_validate(user)
    except HTTPException:
        raise
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Register failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create account.",
        ) from exc


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        user = get_user_by_email(db, payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
        token = create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=token)
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        logger.exception("Login failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not complete login.",
        ) from exc
