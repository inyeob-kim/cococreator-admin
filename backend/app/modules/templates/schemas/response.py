from datetime import datetime

from pydantic import BaseModel

from app.common.schemas.pagination import PaginatedMeta


class TemplateResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str | None
    base_cost: float
    suggested_price: float
    currency: str
    halal_supported: bool
    status: str
    created_at: datetime
    updated_at: datetime


class TemplateListResponse(BaseModel):
    items: list[TemplateResponse]
    meta: PaginatedMeta


class TemplateFlavorResponse(BaseModel):
    id: int
    product_template_id: int
    flavor_name: str
    spice_level: str | None
    description: str | None
    additional_cost: float
    created_at: datetime
    updated_at: datetime
