from pydantic import Field

from app.common.schemas.filters import SearchQuery
from app.common.schemas.pagination import PaginationQuery
from app.common.schemas.sorting import SortingQuery
from app.modules.brands.enums import BrandStatus


class BrandListQuery(PaginationQuery, SortingQuery, SearchQuery):
    creator_id: int | None = None
    status: BrandStatus | None = None
    slug: str | None = Field(default=None, max_length=150)
