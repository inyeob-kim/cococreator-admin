from datetime import datetime

from pydantic import BaseModel

from app.common.schemas.pagination import PaginatedMeta


class OrderResponse(BaseModel):
    id: int
    product_id: int
    sales_channel_id: int | None
    order_number: str | None
    order_date: datetime
    quantity: int
    gross_revenue: float
    platform_fee_amount: float
    shipping_fee_amount: float
    net_revenue: float
    currency: str
    order_status: str
    customer_country_code: str | None
    created_at: datetime


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    meta: PaginatedMeta


class OrderSummaryResponse(BaseModel):
    total_orders: int
    total_quantity: int
    total_gross_revenue: float
    total_platform_fee: float
    total_shipping_fee: float
    total_net_revenue: float


class OrderStatusTransitionResponse(BaseModel):
    order_id: int
    from_status: str
    to_status: str
    reason: str | None
    changed_by_user_id: int
    changed_at: datetime
