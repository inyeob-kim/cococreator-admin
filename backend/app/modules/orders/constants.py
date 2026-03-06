ORDER_TAG = "orders"

ALLOWED_ORDER_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "paid": {"shipped", "canceled", "refunded"},
    "shipped": {"delivered", "canceled", "refunded"},
    "delivered": set(),
    "canceled": set(),
    "refunded": set(),
}
