from enum import StrEnum


class RevenueShareType(StrEnum):
    PROFIT_SHARE = "profit_share"
    REVENUE_SHARE = "revenue_share"
    FIXED_FEE = "fixed_fee"


class PayoutStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
