from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.product_pipeline.model import ProductPipelineLog
from app.modules.products.model import Product


class ProductPipelineRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_products(self) -> list[Product]:
        return self.db.execute(select(Product).order_by(Product.id.asc())).scalars().all()

    def get_product(self, product_id: int) -> Product | None:
        return self.db.execute(select(Product).where(Product.id == product_id)).scalar_one_or_none()

    def save_product(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def create_log(self, log: ProductPipelineLog) -> ProductPipelineLog:
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def list_logs(self, product_id: int) -> list[ProductPipelineLog]:
        stmt = select(ProductPipelineLog).where(ProductPipelineLog.product_id == product_id).order_by(ProductPipelineLog.id.desc())
        return self.db.execute(stmt).scalars().all()
