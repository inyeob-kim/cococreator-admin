from datetime import datetime

from pydantic import BaseModel, Field

from app.modules.orders.enums import OrderStatus


class CreateOrderRequest(BaseModel):
    product_id: int
    sales_channel_id: int | None = None
    order_number: str | None = Field(default=None, max_length=100)
    order_date: datetime
    quantity: int = Field(default=1, ge=1)
    gross_revenue: float = Field(default=0, ge=0)
    platform_fee_amount: float = Field(default=0, ge=0)
    shipping_fee_amount: float = Field(default=0, ge=0)
    net_revenue: float | None = Field(default=None, ge=0)
    currency: str = Field(default="USD", max_length=10)
    order_status: OrderStatus = OrderStatus.PAID
    customer_country_code: str | None = Field(default=None, max_length=10)


class ChangeOrderStatusRequest(BaseModel):
    to_status: OrderStatus
    reason: str | None = None
