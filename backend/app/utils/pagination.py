from math import ceil


def paginate(total_count: int, page: int, page_size: int) -> dict[str, int]:
    total_pages = ceil(total_count / page_size) if page_size else 0
    return {
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
