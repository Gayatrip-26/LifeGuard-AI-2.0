import hmac
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.auth import verify_token
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import get_user

_bearer_optional = HTTPBearer(auto_error=False)


@dataclass
class ServiceOrUserContext:
    is_service: bool
    user: User | None


def _internal_token_valid(token: str | None) -> bool:
    if not settings.internal_service_token or not token:
        return False
    return hmac.compare_digest(token, settings.internal_service_token)


async def get_service_or_user(
    x_internal_token: str | None = Header(None, alias="X-Internal-Token"),
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_optional),
    db: Session = Depends(get_db),
) -> ServiceOrUserContext:
    if _internal_token_valid(x_internal_token):
        return ServiceOrUserContext(is_service=True, user=None)
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = verify_token(credentials.credentials)
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    return ServiceOrUserContext(is_service=False, user=user)


def ensure_user_id_matches(ctx: ServiceOrUserContext, body_user_id: int) -> None:
    if ctx.is_service:
        return
    if ctx.user is None or ctx.user.id != body_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot save data for another user.",
        )


def require_internal_service(
    x_internal_token: str | None = Header(None, alias="X-Internal-Token"),
) -> None:
    if not settings.internal_service_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Internal service authentication is not configured.",
        )
    if not _internal_token_valid(x_internal_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid internal service credentials.",
        )
