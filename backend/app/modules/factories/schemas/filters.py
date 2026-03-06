from pydantic import Field

from app.common.schemas.filters import SearchQuery
from app.common.schemas.pagination import PaginationQuery
from app.common.schemas.sorting import SortingQuery


class FactoryListQuery(PaginationQuery, SortingQuery, SearchQuery):
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    category: str | None = None
    halal_certified: bool | None = None
