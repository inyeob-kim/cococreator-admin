from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.modules.brands.model import Brand
from app.modules.products.model import Product
from app.modules.products.schemas.filters import ProductListQuery


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_products(self, query: ProductListQuery) -> tuple[list[Product], int]:
        stmt = select(Product)
        stmt = self._apply_filters(stmt, query)

        total_count = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()

        if query.sort_by and hasattr(Product, query.sort_by):
            sort_column = getattr(Product, query.sort_by)
            stmt = stmt.order_by(sort_column.asc() if query.sort_order == "asc" else sort_column.desc())
        else:
            stmt = stmt.order_by(Product.id.desc())

        offset = (query.page - 1) * query.page_size
        items = self.db.execute(stmt.offset(offset).limit(query.page_size)).scalars().all()
        return items, total_count

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.execute(select(Product).where(Product.id == product_id)).scalar_one_or_none()

    def get_by_sku(self, sku: str) -> Product | None:
        return self.db.execute(select(Product).where(Product.sku == sku)).scalar_one_or_none()

    def exists_brand(self, brand_id: int) -> bool:
        return self.db.execute(select(Brand.id).where(Brand.id == brand_id)).scalar_one_or_none() is not None

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def save(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def _apply_filters(self, stmt: Select, query: ProductListQuery) -> Select:
        if query.q:
            stmt = stmt.where(Product.name.ilike(f"%{query.q}%"))
        if query.brand_id:
            stmt = stmt.where(Product.brand_id == query.brand_id)
        if query.product_template_id:
            stmt = stmt.where(Product.product_template_id == query.product_template_id)
        if query.factory_id:
            stmt = stmt.where(Product.factory_id == query.factory_id)
        if query.category:
            stmt = stmt.where(Product.category == query.category)
        if query.status:
            stmt = stmt.where(Product.status == query.status.value)
        return stmt
