from datetime import datetime

from pydantic import BaseModel


class OrderBase(BaseModel):
    product_id: int
    order_date: datetime
    quantity: int = 1
