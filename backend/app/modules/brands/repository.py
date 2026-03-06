from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.modules.brands.model import Brand
from app.modules.brands.schemas.filters import BrandListQuery
from app.modules.creators.model import Creator


class BrandRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_brands(self, query: BrandListQuery) -> tuple[list[Brand], int]:
        stmt = select(Brand)
        stmt = self._apply_filters(stmt, query)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_count = self.db.execute(count_stmt).scalar_one()

        if query.sort_by and hasattr(Brand, query.sort_by):
            sort_column = getattr(Brand, query.sort_by)
            stmt = stmt.order_by(sort_column.asc() if query.sort_order == "asc" else sort_column.desc())
        else:
            stmt = stmt.order_by(Brand.id.desc())

        offset = (query.page - 1) * query.page_size
        items = self.db.execute(stmt.offset(offset).limit(query.page_size)).scalars().all()
        return items, total_count

    def get_by_id(self, brand_id: int) -> Brand | None:
        return self.db.execute(select(Brand).where(Brand.id == brand_id)).scalar_one_or_none()

    def exists_creator(self, creator_id: int) -> bool:
        stmt = select(Creator.id).where(Creator.id == creator_id)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def get_by_slug(self, slug: str) -> Brand | None:
        return self.db.execute(select(Brand).where(Brand.slug == slug)).scalar_one_or_none()

    def create(self, brand: Brand) -> Brand:
        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)
        return brand

    def save(self, brand: Brand) -> Brand:
        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)
        return brand

    def _apply_filters(self, stmt: Select, query: BrandListQuery) -> Select:
        if query.q:
            like_q = f"%{query.q}%"
            stmt = stmt.where(Brand.name.ilike(like_q))
        if query.creator_id:
            stmt = stmt.where(Brand.creator_id == query.creator_id)
        if query.status:
            stmt = stmt.where(Brand.status == query.status.value)
        if query.slug:
            stmt = stmt.where(Brand.slug == query.slug)
        return stmt
