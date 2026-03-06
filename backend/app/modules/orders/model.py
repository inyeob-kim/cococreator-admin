from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.modules.orders.enums import OrderStatus


class SalesChannel(Base):
    __tablename__ = "sales_channels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"), index=True)
    sales_channel_id: Mapped[int | None] = mapped_column(ForeignKey("sales_channels.id", ondelete="SET NULL"), nullable=True)
    order_number: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    gross_revenue: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    platform_fee_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    shipping_fee_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    net_revenue: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    order_status: Mapped[str] = mapped_column(String(50), nullable=False, default=OrderStatus.PAID.value, index=True)
    customer_country_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)
