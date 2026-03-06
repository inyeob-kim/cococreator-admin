from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.brands.model import Brand
from app.modules.creators.model import Creator
from app.modules.orders.model import Order
from app.modules.products.model import Product


class AnalyticsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def revenue_trend(self) -> list[dict]:
        rows = self.db.execute(
            select(func.date(Order.order_date), func.coalesce(func.sum(Order.net_revenue), 0))
            .group_by(func.date(Order.order_date))
            .order_by(func.date(Order.order_date).asc())
        ).all()
        return [{"bucket": str(r[0]), "value": float(r[1])} for r in rows]

    def order_trend(self) -> list[dict]:
        rows = self.db.execute(
            select(func.date(Order.order_date), func.count(Order.id))
            .group_by(func.date(Order.order_date))
            .order_by(func.date(Order.order_date).asc())
        ).all()
        return [{"bucket": str(r[0]), "value": float(r[1])} for r in rows]

    def top_creators(self, limit: int) -> list[dict]:
        rows = self.db.execute(
            select(
                Creator.id,
                Creator.name,
                func.coalesce(func.sum(Order.net_revenue), 0),
            )
            .join(Brand, Brand.creator_id == Creator.id)
            .join(Product, Product.brand_id == Brand.id)
            .join(Order, Order.product_id == Product.id)
            .group_by(Creator.id, Creator.name)
            .order_by(func.sum(Order.net_revenue).desc())
            .limit(limit)
        ).all()
        return [{"creator_id": int(r[0]), "creator_name": str(r[1]), "revenue": float(r[2])} for r in rows]

    def top_products(self, limit: int) -> list[dict]:
        rows = self.db.execute(
            select(
                Product.id,
                Product.name,
                func.count(Order.id),
                func.coalesce(func.sum(Order.net_revenue), 0),
            )
            .join(Order, Order.product_id == Product.id)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(Order.net_revenue).desc())
            .limit(limit)
        ).all()
        return [
            {
                "product_id": int(r[0]),
                "product_name": str(r[1]),
                "sales": int(r[2]),
                "revenue": float(r[3]),
            }
            for r in rows
        ]
