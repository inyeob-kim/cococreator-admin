from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.mixins import TimestampMixin
from app.modules.templates.enums import TemplateStatus


class ProductTemplate(Base, TimestampMixin):
    __tablename__ = "product_templates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    base_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    suggested_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    halal_supported: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default=TemplateStatus.ACTIVE.value, index=True)


class TemplateFlavor(Base, TimestampMixin):
    __tablename__ = "template_flavors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_template_id: Mapped[int] = mapped_column(ForeignKey("product_templates.id", ondelete="CASCADE"), index=True)
    flavor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    spice_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    additional_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
