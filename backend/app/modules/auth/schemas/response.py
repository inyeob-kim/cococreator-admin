from datetime import datetime

from pydantic import BaseModel, EmailStr


class AuthUserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    is_active: bool


class TokenPairResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    refresh_expires_at: datetime
    user: AuthUserResponse

