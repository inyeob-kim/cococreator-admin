from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.modules.templates.model import ProductTemplate, TemplateFlavor
from app.modules.templates.schemas.filters import TemplateListQuery


class TemplateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_templates(self, query: TemplateListQuery) -> tuple[list[ProductTemplate], int]:
        stmt = select(ProductTemplate)
        if query.q:
            stmt = stmt.where(ProductTemplate.name.ilike(f"%{query.q}%"))
        if query.category:
            stmt = stmt.where(ProductTemplate.category == query.category)
        if query.status:
            stmt = stmt.where(ProductTemplate.status == query.status.value)

        total = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
        if query.sort_by and hasattr(ProductTemplate, query.sort_by):
            sort_column = getattr(ProductTemplate, query.sort_by)
            stmt = stmt.order_by(sort_column.asc() if query.sort_order == "asc" else sort_column.desc())
        else:
            stmt = stmt.order_by(ProductTemplate.id.desc())
        offset = (query.page - 1) * query.page_size
        items = self.db.execute(stmt.offset(offset).limit(query.page_size)).scalars().all()
        return items, total

    def get_template(self, template_id: int) -> ProductTemplate | None:
        return self.db.execute(select(ProductTemplate).where(ProductTemplate.id == template_id)).scalar_one_or_none()

    def create_template(self, item: ProductTemplate) -> ProductTemplate:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save_template(self, item: ProductTemplate) -> ProductTemplate:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_flavors(self, template_id: int) -> list[TemplateFlavor]:
        stmt = select(TemplateFlavor).where(TemplateFlavor.product_template_id == template_id).order_by(TemplateFlavor.id.asc())
        return self.db.execute(stmt).scalars().all()

    def get_flavor(self, template_id: int, flavor_id: int) -> TemplateFlavor | None:
        stmt = select(TemplateFlavor).where(TemplateFlavor.product_template_id == template_id, TemplateFlavor.id == flavor_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create_flavor(self, item: TemplateFlavor) -> TemplateFlavor:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save_flavor(self, item: TemplateFlavor) -> TemplateFlavor:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_flavor(self, item: TemplateFlavor) -> None:
        self.db.delete(item)
        self.db.commit()
