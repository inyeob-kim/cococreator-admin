from pydantic import Field

from app.common.schemas.filters import SearchQuery
from app.common.schemas.pagination import PaginationQuery
from app.common.schemas.sorting import SortingQuery
from app.modules.creators.enums import CreatorCategory, CreatorPlatform, CreatorStatus


class CreatorListQuery(PaginationQuery, SortingQuery, SearchQuery):
    status: CreatorStatus | None = None
    platform: CreatorPlatform | None = None
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    category: CreatorCategory | None = None

