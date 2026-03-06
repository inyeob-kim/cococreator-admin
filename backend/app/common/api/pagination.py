from typing import Any


def paginated_payload(
    *,
    items: list[Any],
    total_count: int,
    page: int,
    page_size: int,
) -> dict[str, Any]:
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
    }

