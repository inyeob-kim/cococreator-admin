import secrets
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.exceptions.auth import ForbiddenException, UnauthorizedException
from app.core.security import create_access_token, hash_token, verify_password
from app.modules.auth.constants import ACCESS_TOKEN_TYPE
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas.request import LoginRequest
from app.modules.auth.schemas.response import AuthUserResponse, TokenPairResponse


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    def login(
        self,
        *,
        payload: LoginRequest,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> TokenPairResponse:
        user = self.repository.find_user_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise UnauthorizedException(
                code="INVALID_CREDENTIALS", message="Invalid email or password"
            )
        if not user.is_active:
            raise ForbiddenException(code="USER_INACTIVE", message="User is inactive")

        refresh_days = settings.REFRESH_TOKEN_EXPIRE_DAYS * (2 if payload.remember_me else 1)
        refresh_expires_at = datetime.utcnow() + timedelta(days=refresh_days)
        raw_refresh_token = secrets.token_urlsafe(48)
        self.repository.create_session(
            user_id=user.id,
            refresh_token_hash=hash_token(raw_refresh_token),
            expires_at=refresh_expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.repository.update_last_login_at(user, datetime.utcnow())

        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        access_token = create_access_token(
            user_id=user.id,
            role=user.role,
            expires_in_seconds=expires_in,
        )
        return TokenPairResponse(
            access_token=access_token,
            token_type=ACCESS_TOKEN_TYPE,
            expires_in=expires_in,
            refresh_token=raw_refresh_token,
            refresh_expires_at=refresh_expires_at,
            user=AuthUserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                role=user.role,
                is_active=user.is_active,
            ),
        )

    def refresh(self, *, refresh_token: str) -> TokenPairResponse:
        session = self.repository.find_session_by_refresh_hash(hash_token(refresh_token))
        if session is None:
            raise UnauthorizedException(
                code="INVALID_REFRESH_TOKEN", message="Refresh token is invalid"
            )
        if session.expires_at < datetime.utcnow():
            self.repository.delete_session_by_refresh_hash(hash_token(refresh_token))
            raise UnauthorizedException(
                code="REFRESH_TOKEN_EXPIRED", message="Refresh token expired"
            )

        user = self.repository.find_user_by_id(session.user_id)
        if user is None or not user.is_active:
            raise UnauthorizedException(code="UNAUTHORIZED", message="User unavailable")

        self.repository.delete_session_by_refresh_hash(hash_token(refresh_token))
        new_refresh_raw = secrets.token_urlsafe(48)
        new_refresh_expires_at = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        self.repository.create_session(
            user_id=user.id,
            refresh_token_hash=hash_token(new_refresh_raw),
            expires_at=new_refresh_expires_at,
            ip_address=None,
            user_agent=None,
        )
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        access_token = create_access_token(
            user_id=user.id,
            role=user.role,
            expires_in_seconds=expires_in,
        )
        return TokenPairResponse(
            access_token=access_token,
            token_type=ACCESS_TOKEN_TYPE,
            expires_in=expires_in,
            refresh_token=new_refresh_raw,
            refresh_expires_at=new_refresh_expires_at,
            user=AuthUserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                role=user.role,
                is_active=user.is_active,
            ),
        )

    def logout(self, *, refresh_token: str) -> None:
        self.repository.delete_session_by_refresh_hash(hash_token(refresh_token))

