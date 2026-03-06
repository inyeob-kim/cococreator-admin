from datetime import date, datetime

from pydantic import BaseModel

from app.common.schemas.pagination import PaginatedMeta


class PayoutResponse(BaseModel):
    id: int
    creator_id: int
    brand_id: int | None
    product_id: int | None
    period_start: date
    period_end: date
    total_revenue: float
    creator_share_amount: float
    currency: str
    payment_status: str
    paid_at: datetime | None
    created_at: datetime


class PayoutListResponse(BaseModel):
    items: list[PayoutResponse]
    meta: PaginatedMeta


class FinanceSummaryResponse(BaseModel):
    total_revenue: float
    total_creator_payouts: float
    platform_revenue: float
    avg_margin_rate: float


class PayoutActionResponse(BaseModel):
    payout_id: int
    from_status: str
    to_status: str
    changed_at: datetime
