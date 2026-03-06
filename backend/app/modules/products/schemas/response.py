from datetime import datetime

from pydantic import BaseModel

from app.common.schemas.pagination import PaginatedMeta


class ProductResponse(BaseModel):
    id: int
    brand_id: int
    product_template_id: int | None
    template_flavor_id: int | None
    factory_id: int | None
    name: str
    sku: str | None
    category: str
    status: str
    cogs: float
    shipping_cost: float
    platform_fee_rate: float
    retail_price: float
    currency: str
    halal_required: bool
    halal_status: str | None
    package_type: str | None
    package_size: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    meta: PaginatedMeta


class ProductPricingResponse(BaseModel):
    product_id: int
    cogs: float
    shipping_cost: float
    platform_fee_rate: float
    retail_price: float
    currency: str
    margin_rate: float
