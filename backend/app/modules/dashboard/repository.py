from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.brands.model import Brand
from app.modules.creators.model import Creator
from app.modules.orders.model import Order
from app.modules.products.model import Product


class DashboardRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def summary(self) -> dict:
        total_creators = self.db.execute(select(func.count(Creator.id))).scalar_one()
        active_brands = self.db.execute(select(func.count(Brand.id)).where(Brand.status == "active")).scalar_one()
        launched_products = self.db.execute(select(func.count(Product.id)).where(Product.status.in_(["launch", "active"]))).scalar_one()
        total_revenue = self.db.execute(select(func.coalesce(func.sum(Order.net_revenue), 0))).scalar_one()
        return {
            "total_creators": int(total_creators),
            "active_brands": int(active_brands),
            "launched_products": int(launched_products),
            "total_revenue": float(total_revenue),
        }

    def creator_pipeline_counts(self) -> list[dict]:
        rows = self.db.execute(select(Creator.status, func.count(Creator.id)).group_by(Creator.status)).all()
        return [{"status": str(r[0]), "count": int(r[1])} for r in rows]

    def top_products(self, limit: int = 5) -> list[dict]:
        rows = self.db.execute(
            select(
                Product.id,
                Product.name,
                func.count(Order.id),
                func.coalesce(func.sum(Order.net_revenue), 0),
                func.coalesce(func.avg((Product.retail_price - (Product.cogs + Product.shipping_cost)) / func.nullif(Product.retail_price, 0) * 100), 0),
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
                "orders": int(r[2]),
                "revenue": float(r[3]),
                "margin_rate": float(r[4]),
            }
            for r in rows
        ]
