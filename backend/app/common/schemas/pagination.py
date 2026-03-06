from pydantic import Field

from app.common.schemas.base import AppSchema


class PaginationQuery(AppSchema):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)


class PaginatedMeta(AppSchema):
    page: int
    page_size: int
    total_count: int

