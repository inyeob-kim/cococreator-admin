from app.common.schemas.filters import SearchQuery
from app.common.schemas.pagination import PaginationQuery
from app.common.schemas.sorting import SortingQuery
from app.modules.templates.enums import TemplateStatus


class TemplateListQuery(PaginationQuery, SortingQuery, SearchQuery):
    category: str | None = None
    status: TemplateStatus | None = None
