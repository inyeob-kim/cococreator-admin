from typing import Literal

from pydantic import Field

from app.common.schemas.base import AppSchema


class SortingQuery(AppSchema):
    sort_by: str | None = None
    sort_order: Literal["asc", "desc"] = Field(default="desc")

