from datetime import date, datetime

from pydantic import BaseModel

from app.common.schemas.pagination import PaginatedMeta


class BrandResponse(BaseModel):
    id: int
    creator_id: int
    name: str
    slug: str | None
    description: str | None
    status: str
    launch_date: date | None
    logo_url: str | None
    brand_story: str | None
    created_at: datetime
    updated_at: datetime


class BrandListResponse(BaseModel):
    items: list[BrandResponse]
    meta: PaginatedMeta


class BrandStatusTransitionResponse(BaseModel):
    brand_id: int
    from_status: str
    to_status: str
    reason: str | None
    changed_at: datetime
    changed_by_user_id: int
