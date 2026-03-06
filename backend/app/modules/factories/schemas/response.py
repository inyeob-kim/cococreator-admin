from datetime import datetime

from pydantic import BaseModel

from app.common.schemas.pagination import PaginatedMeta


class FactoryResponse(BaseModel):
    id: int
    name: str
    country_code: str | None
    website_url: str | None
    contact_name: str | None
    contact_email: str | None
    contact_phone: str | None
    halal_certified: bool
    notes: str | None
    created_at: datetime
    updated_at: datetime


class FactoryListResponse(BaseModel):
    items: list[FactoryResponse]
    meta: PaginatedMeta


class FactoryCapabilityResponse(BaseModel):
    id: int
    factory_id: int
    category: str
    moq: int | None
    lead_time_days: int | None
    estimated_unit_cost: float | None
    currency: str
    notes: str | None
    created_at: datetime
    updated_at: datetime
