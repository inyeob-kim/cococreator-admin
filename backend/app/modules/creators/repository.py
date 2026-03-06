from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.modules.creators.model import Creator, CreatorContact
from app.modules.creators.schemas.filters import CreatorListQuery


class CreatorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_creators(self, query: CreatorListQuery) -> tuple[list[Creator], int]:
        stmt = select(Creator)
        stmt = self._apply_filters(stmt, query)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_count = self.db.execute(count_stmt).scalar_one()

        if query.sort_by and hasattr(Creator, query.sort_by):
            sort_column = getattr(Creator, query.sort_by)
            stmt = stmt.order_by(
                sort_column.asc() if query.sort_order == "asc" else sort_column.desc()
            )
        else:
            stmt = stmt.order_by(Creator.id.desc())

        offset = (query.page - 1) * query.page_size
        stmt = stmt.offset(offset).limit(query.page_size)
        items = self.db.execute(stmt).scalars().all()
        return items, total_count

    def get_by_id(self, creator_id: int) -> Creator | None:
        stmt = select(Creator).where(Creator.id == creator_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, creator: Creator) -> Creator:
        self.db.add(creator)
        self.db.commit()
        self.db.refresh(creator)
        return creator

    def save(self, creator: Creator) -> Creator:
        self.db.add(creator)
        self.db.commit()
        self.db.refresh(creator)
        return creator

    def list_contacts(self, creator_id: int) -> list[CreatorContact]:
        stmt = (
            select(CreatorContact)
            .where(CreatorContact.creator_id == creator_id)
            .order_by(CreatorContact.id.asc())
        )
        return self.db.execute(stmt).scalars().all()

    def get_contact(self, creator_id: int, contact_id: int) -> CreatorContact | None:
        stmt = select(CreatorContact).where(
            CreatorContact.creator_id == creator_id, CreatorContact.id == contact_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create_contact(self, contact: CreatorContact) -> CreatorContact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def save_contact(self, contact: CreatorContact) -> CreatorContact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def save_contacts(self, contacts: list[CreatorContact]) -> None:
        for contact in contacts:
            self.db.add(contact)
        self.db.commit()

    def delete_contact(self, contact: CreatorContact) -> None:
        self.db.delete(contact)
        self.db.commit()

    def _apply_filters(self, stmt: Select, query: CreatorListQuery) -> Select:
        if query.q:
            like_q = f"%{query.q}%"
            stmt = stmt.where(Creator.name.ilike(like_q))
        if query.status:
            stmt = stmt.where(Creator.status == query.status.value)
        if query.platform:
            stmt = stmt.where(Creator.platform == query.platform.value)
        if query.country_code:
            stmt = stmt.where(Creator.country_code == query.country_code.upper())
        if query.category:
            stmt = stmt.where(Creator.category == query.category.value)
        return stmt

