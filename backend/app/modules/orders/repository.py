from datetime import date, datetime, time

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.modules.orders.model import Order
from app.modules.orders.schemas.filters import OrderListQuery
from app.modules.products.model import Product


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_orders(self, query: OrderListQuery) -> tuple[list[Order], int]:
        stmt = select(Order)
        stmt = self._apply_filters(stmt, query)

        total = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
        if query.sort_by and hasattr(Order, query.sort_by):
            sort_column = getattr(Order, query.sort_by)
            stmt = stmt.order_by(sort_column.asc() if query.sort_order == "asc" else sort_column.desc())
        else:
            stmt = stmt.order_by(Order.order_date.desc())

        offset = (query.page - 1) * query.page_size
        items = self.db.execute(stmt.offset(offset).limit(query.page_size)).scalars().all()
        return items, total

    def get_order(self, order_id: int) -> Order | None:
        return self.db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()

    def get_order_by_number(self, order_number: str) -> Order | None:
        return self.db.execute(select(Order).where(Order.order_number == order_number)).scalar_one_or_none()

    def exists_product(self, product_id: int) -> bool:
        return self.db.execute(select(Product.id).where(Product.id == product_id)).scalar_one_or_none() is not None

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def save_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_summary(self, query: OrderListQuery) -> dict:
        stmt = select(
            func.count(Order.id),
            func.coalesce(func.sum(Order.quantity), 0),
            func.coalesce(func.sum(Order.gross_revenue), 0),
            func.coalesce(func.sum(Order.platform_fee_amount), 0),
            func.coalesce(func.sum(Order.shipping_fee_amount), 0),
            func.coalesce(func.sum(Order.net_revenue), 0),
        )
        filtered = self._apply_filters(select(Order.id).add_columns(Order.quantity, Order.gross_revenue, Order.platform_fee_amount, Order.shipping_fee_amount, Order.net_revenue), query).subquery()
        stmt = select(
            func.count(filtered.c.id),
            func.coalesce(func.sum(filtered.c.quantity), 0),
            func.coalesce(func.sum(filtered.c.gross_revenue), 0),
            func.coalesce(func.sum(filtered.c.platform_fee_amount), 0),
            func.coalesce(func.sum(filtered.c.shipping_fee_amount), 0),
            func.coalesce(func.sum(filtered.c.net_revenue), 0),
        )
        row = self.db.execute(stmt).one()
        return {
            "total_orders": int(row[0]),
            "total_quantity": int(row[1]),
            "total_gross_revenue": float(row[2]),
            "total_platform_fee": float(row[3]),
            "total_shipping_fee": float(row[4]),
            "total_net_revenue": float(row[5]),
        }

    def _apply_filters(self, stmt: Select, query: OrderListQuery) -> Select:
        if query.from_date:
            from_dt = datetime.combine(query.from_date, time.min)
            stmt = stmt.where(Order.order_date >= from_dt)
        if query.to_date:
            to_dt = datetime.combine(query.to_date, time.max)
            stmt = stmt.where(Order.order_date <= to_dt)
        if query.product_id:
            stmt = stmt.where(Order.product_id == query.product_id)
        if query.sales_channel_id:
            stmt = stmt.where(Order.sales_channel_id == query.sales_channel_id)
        if query.order_status:
            stmt = stmt.where(Order.order_status == query.order_status.value)
        return stmt
