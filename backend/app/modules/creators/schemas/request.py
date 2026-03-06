from pydantic import BaseModel, EmailStr, Field

from app.modules.creators.enums import (
    CreatorCategory,
    CreatorContactType,
    CreatorPlatform,
    CreatorStatus,
)


class CreateCreatorRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    display_name: str | None = Field(default=None, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    platform: CreatorPlatform | None = None
    channel_name: str | None = Field(default=None, max_length=150)
    channel_url: str | None = None
    subscribers_count: int = Field(default=0, ge=0)
    avg_views: int = Field(default=0, ge=0)
    category: CreatorCategory | None = None
    audience_summary: str | None = None
    notes: str | None = None


class UpdateCreatorRequest(BaseModel):
    display_name: str | None = Field(default=None, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    platform: CreatorPlatform | None = None
    channel_name: str | None = Field(default=None, max_length=150)
    channel_url: str | None = None
    subscribers_count: int | None = Field(default=None, ge=0)
    avg_views: int | None = Field(default=None, ge=0)
    category: CreatorCategory | None = None
    audience_summary: str | None = None
    notes: str | None = None


class ChangeCreatorStatusRequest(BaseModel):
    to_status: CreatorStatus
    reason: str | None = None


class CreateCreatorContactRequest(BaseModel):
    contact_type: CreatorContactType
    contact_value: str = Field(min_length=1, max_length=255)
    is_primary: bool = False


class UpdateCreatorContactRequest(BaseModel):
    contact_type: CreatorContactType | None = None
    contact_value: str | None = Field(default=None, min_length=1, max_length=255)
    is_primary: bool | None = None

