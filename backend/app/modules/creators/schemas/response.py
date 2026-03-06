from datetime import datetime

from pydantic import BaseModel

from app.common.schemas.pagination import PaginatedMeta


class CreatorResponse(BaseModel):
    id: int
    name: str
    display_name: str | None
    email: str | None
    phone: str | None
    country_code: str | None
    platform: str | None
    channel_name: str | None
    channel_url: str | None
    subscribers_count: int
    avg_views: int
    category: str | None
    status: str
    audience_summary: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class CreatorListResponse(BaseModel):
    items: list[CreatorResponse]
    meta: PaginatedMeta


class CreatorStatusTransitionResponse(BaseModel):
    creator_id: int
    from_status: str
    to_status: str
    reason: str | None
    changed_at: datetime
    changed_by_user_id: int


class CreatorContactResponse(BaseModel):
    id: int
    creator_id: int
    contact_type: str
    contact_value: str
    is_primary: bool
    created_at: datetime
    updated_at: datetime


class CreatorContactListResponse(BaseModel):
    items: list[CreatorContactResponse]

