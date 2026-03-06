from app.common.schemas.filters import SearchQuery
from app.common.schemas.pagination import PaginationQuery
from app.common.schemas.sorting import SortingQuery
from app.modules.products.enums import ProductStatus


class ProductListQuery(PaginationQuery, SortingQuery, SearchQuery):
    brand_id: int | None = None
    product_template_id: int | None = None
    factory_id: int | None = None
    category: str | None = None
    status: ProductStatus | None = None
