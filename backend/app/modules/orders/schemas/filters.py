from datetime import date

from app.common.schemas.pagination import PaginationQuery
from app.common.schemas.sorting import SortingQuery
from app.modules.orders.enums import OrderStatus


class OrderListQuery(PaginationQuery, SortingQuery):
    from_date: date | None = None
    to_date: date | None = None
    product_id: int | None = None
    sales_channel_id: int | None = None
    order_status: OrderStatus | None = None
