from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.constants import AUTH_TAG
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas.request import LoginRequest, LogoutRequest, RefreshTokenRequest
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=[AUTH_TAG])


@router.post("/login")
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> dict:
    service = AuthService(AuthRepository(db))
    result = service.login(
        payload=payload,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return success_response(result.model_dump(), "Login successful")


@router.post("/refresh")
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> dict:
    service = AuthService(AuthRepository(db))
    result = service.refresh(refresh_token=payload.refresh_token)
    return success_response(result.model_dump(), "Token refreshed")


@router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)) -> dict:
    if payload.refresh_token:
        service = AuthService(AuthRepository(db))
        service.logout(refresh_token=payload.refresh_token)
    return success_response({"logged_out": True}, "Logout successful")


@router.get("/me")
def me(current_user=Depends(get_current_user)) -> dict:
    return success_response(
        {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "role": current_user.role,
            "is_active": current_user.is_active,
        }
    )

