BRAND_TAG = "brands"

ALLOWED_BRAND_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "planning": {"active", "archived"},
    "active": {"paused", "archived"},
    "paused": {"active", "archived"},
    "archived": set(),
}
