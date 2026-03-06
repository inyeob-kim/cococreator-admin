from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.modules.brands.model import Brand
from app.modules.finance.model import Payout
from app.modules.orders.model import Order
from app.modules.products.model import Product


class FinanceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_payouts(self, *, creator_id: int | None, payment_status: str | None, period_start_from: date | None, period_end_to: date | None, page: int, page_size: int) -> tuple[list[Payout], int]:
        stmt = select(Payout)
        if creator_id:
            stmt = stmt.where(Payout.creator_id == creator_id)
        if payment_status:
            stmt = stmt.where(Payout.payment_status == payment_status)
        if period_start_from:
            stmt = stmt.where(Payout.period_start >= period_start_from)
        if period_end_to:
            stmt = stmt.where(Payout.period_end <= period_end_to)

        total = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
        offset = (page - 1) * page_size
        items = self.db.execute(stmt.order_by(Payout.id.desc()).offset(offset).limit(page_size)).scalars().all()
        return items, total

    def get_payout(self, payout_id: int) -> Payout | None:
        return self.db.execute(select(Payout).where(Payout.id == payout_id)).scalar_one_or_none()

    def save_payout(self, payout: Payout) -> Payout:
        self.db.add(payout)
        self.db.commit()
        self.db.refresh(payout)
        return payout

    def create_payouts(self, payouts: list[Payout]) -> list[Payout]:
        for item in payouts:
            self.db.add(item)
        self.db.commit()
        for item in payouts:
            self.db.refresh(item)
        return payouts

    def has_payout_for_period(self, creator_id: int, period_start: date, period_end: date) -> bool:
        stmt = select(Payout.id).where(Payout.creator_id == creator_id, Payout.period_start == period_start, Payout.period_end == period_end)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def payout_summary(self) -> dict:
        row = self.db.execute(select(
            func.coalesce(func.sum(Payout.total_revenue), 0),
            func.coalesce(func.sum(Payout.creator_share_amount), 0),
        )).one()
        total_revenue = float(row[0])
        total_creator = float(row[1])
        platform = max(total_revenue - total_creator, 0)
        avg_margin = 0 if total_revenue <= 0 else round((platform / total_revenue) * 100, 2)
        return {
            "total_revenue": total_revenue,
            "total_creator_payouts": total_creator,
            "platform_revenue": platform,
            "avg_margin_rate": avg_margin,
        }

    def aggregate_revenue_by_creator(self, *, period_start: date, period_end: date, creator_id: int | None) -> list[tuple[int, float]]:
        stmt = (
            select(Brand.creator_id, func.coalesce(func.sum(Order.net_revenue), 0))
            .join(Product, Product.id == Order.product_id)
            .join(Brand, Brand.id == Product.brand_id)
            .where(and_(func.date(Order.order_date) >= period_start, func.date(Order.order_date) <= period_end))
            .group_by(Brand.creator_id)
        )
        if creator_id:
            stmt = stmt.where(Brand.creator_id == creator_id)
        rows = self.db.execute(stmt).all()
        return [(int(r[0]), float(r[1])) for r in rows]
