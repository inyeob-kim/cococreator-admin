from app.common.schemas.base import AppSchema


class SearchQuery(AppSchema):
    q: str | None = None

