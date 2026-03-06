from datetime import date

from pydantic import BaseModel


class DashboardPeriodQuery(BaseModel):
    from_date: date | None = None
    to_date: date | None = None
