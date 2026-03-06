from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class AnalyticsPeriodQuery(BaseModel):
    from_date: date | None = None
    to_date: date | None = None
    granularity: Literal["day", "week", "month"] = "month"
    limit: int = Field(default=10, ge=1, le=100)
