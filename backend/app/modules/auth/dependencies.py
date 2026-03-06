from collections.abc import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions.auth import ForbiddenException, UnauthorizedException
from app.core.security import decode_access_token
from app.modules.auth.repository import AuthRepository

security_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise UnauthorizedException(message="Missing authorization header")

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise UnauthorizedException(message="Invalid or expired token")

    repository = AuthRepository(db)
    user = repository.find_user_by_id(int(payload["user_id"]))
    if user is None or not user.is_active:
        raise UnauthorizedException(message="User is unavailable")
    return user


def require_roles(*roles: str) -> Callable:
    def _dependency(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise ForbiddenException(message="Insufficient role permissions")
        return current_user

    return _dependency

