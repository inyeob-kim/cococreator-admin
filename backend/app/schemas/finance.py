from datetime import date

from pydantic import BaseModel


class PayoutBase(BaseModel):
    creator_id: int
    period_start: date
    period_end: date
