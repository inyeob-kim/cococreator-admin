from datetime import date, datetime

from pydantic import BaseModel, Field

from app.modules.finance.enums import PayoutStatus


class PayoutListQuery(BaseModel):
    creator_id: int | None = None
    payment_status: PayoutStatus | None = None
    period_start_from: date | None = None
    period_end_to: date | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)


class CalculatePayoutRequest(BaseModel):
    period_start: date
    period_end: date
    creator_id: int | None = None


class MarkPayoutPaidRequest(BaseModel):
    paid_at: datetime | None = None


class MarkPayoutFailedRequest(BaseModel):
    reason: str | None = None
