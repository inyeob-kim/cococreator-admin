from sqlalchemy import Select, exists, func, select
from sqlalchemy.orm import Session

from app.modules.factories.model import Factory, FactoryCapability
from app.modules.factories.schemas.filters import FactoryListQuery


class FactoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_factories(self, query: FactoryListQuery) -> tuple[list[Factory], int]:
        stmt = select(Factory)
        stmt = self._apply_filters(stmt, query)

        total = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
        if query.sort_by and hasattr(Factory, query.sort_by):
            sort_column = getattr(Factory, query.sort_by)
            stmt = stmt.order_by(sort_column.asc() if query.sort_order == "asc" else sort_column.desc())
        else:
            stmt = stmt.order_by(Factory.id.desc())

        offset = (query.page - 1) * query.page_size
        items = self.db.execute(stmt.offset(offset).limit(query.page_size)).scalars().all()
        return items, total

    def get_factory(self, factory_id: int) -> Factory | None:
        return self.db.execute(select(Factory).where(Factory.id == factory_id)).scalar_one_or_none()

    def create_factory(self, item: Factory) -> Factory:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save_factory(self, item: Factory) -> Factory:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_capabilities(self, factory_id: int) -> list[FactoryCapability]:
        stmt = select(FactoryCapability).where(FactoryCapability.factory_id == factory_id).order_by(FactoryCapability.id.asc())
        return self.db.execute(stmt).scalars().all()

    def get_capability(self, factory_id: int, capability_id: int) -> FactoryCapability | None:
        stmt = select(FactoryCapability).where(FactoryCapability.factory_id == factory_id, FactoryCapability.id == capability_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create_capability(self, item: FactoryCapability) -> FactoryCapability:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save_capability(self, item: FactoryCapability) -> FactoryCapability:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_capability(self, item: FactoryCapability) -> None:
        self.db.delete(item)
        self.db.commit()

    def supports_category(self, factory_id: int, category: str) -> bool:
        stmt = select(exists().where(FactoryCapability.factory_id == factory_id, FactoryCapability.category == category))
        return bool(self.db.execute(stmt).scalar_one())

    def _apply_filters(self, stmt: Select, query: FactoryListQuery) -> Select:
        if query.q:
            stmt = stmt.where(Factory.name.ilike(f"%{query.q}%"))
        if query.country_code:
            stmt = stmt.where(Factory.country_code == query.country_code.upper())
        if query.halal_certified is not None:
            stmt = stmt.where(Factory.halal_certified == query.halal_certified)
        if query.category:
            stmt = stmt.where(
                exists().where(
                    FactoryCapability.factory_id == Factory.id,
                    FactoryCapability.category == query.category,
                )
            )
        return stmt
