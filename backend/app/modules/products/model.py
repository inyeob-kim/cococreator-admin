from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.mixins import TimestampMixin
from app.modules.products.enums import ProductStatus


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id", ondelete="CASCADE"), index=True)
    product_template_id: Mapped[int | None] = mapped_column(ForeignKey("product_templates.id", ondelete="SET NULL"), nullable=True, index=True)
    template_flavor_id: Mapped[int | None] = mapped_column(ForeignKey("template_flavors.id", ondelete="SET NULL"), nullable=True)
    factory_id: Mapped[int | None] = mapped_column(ForeignKey("factories.id", ondelete="SET NULL"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    sku: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default=ProductStatus.IDEA.value, index=True)
    cogs: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    shipping_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    platform_fee_rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    retail_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    halal_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    halal_status: Mapped[str | None] = mapped_column(String(50), nullable=True, default="not_started")
    package_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    package_size: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
