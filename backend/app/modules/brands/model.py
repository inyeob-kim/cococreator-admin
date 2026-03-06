from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.mixins import TimestampMixin
from app.modules.brands.enums import BrandStatus


class Brand(Base, TimestampMixin):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("creators.id", ondelete="RESTRICT"), index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str | None] = mapped_column(String(150), unique=True, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default=BrandStatus.PLANNING.value, index=True)
    launch_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    brand_story: Mapped[str | None] = mapped_column(Text, nullable=True)
