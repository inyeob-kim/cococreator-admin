from datetime import date

from app.modules.finance.schemas.request import CalculatePayoutRequest, MarkPayoutPaidRequest
from app.modules.finance.service import FinanceService


class _Payout:
    def __init__(self, payout_id: int, creator_id: int, status: str = "pending"):
        self.id = payout_id
        self.creator_id = creator_id
        self.brand_id = None
        self.product_id = None
        self.period_start = date(2026, 1, 1)
        self.period_end = date(2026, 1, 31)
        self.total_revenue = 100.0
        self.creator_share_amount = 30.0
        self.currency = "USD"
        self.payment_status = status
        self.paid_at = None
        self.created_at = __import__("datetime").datetime.utcnow()


class FakeFinanceRepo:
    def __init__(self):
        self.items = [_Payout(1, 1)]

    def list_payouts(self, **kwargs):
        return self.items, len(self.items)

    def get_payout(self, payout_id):
        for i in self.items:
            if i.id == payout_id:
                return i
        return None

    def save_payout(self, payout):
        return payout

    def create_payouts(self, payouts):
        for i, p in enumerate(payouts, start=2):
            p.id = i
            p.created_at = __import__("datetime").datetime.utcnow()
            self.items.append(p)
        return payouts

    def has_payout_for_period(self, creator_id, period_start, period_end):
        return False

    def payout_summary(self):
        return {
            "total_revenue": 100.0,
            "total_creator_payouts": 30.0,
            "platform_revenue": 70.0,
            "avg_margin_rate": 70.0,
        }

    def aggregate_revenue_by_creator(self, **kwargs):
        return [(1, 100.0)]


def test_finance_calculate_payouts_generates_rows():
    service = FinanceService(FakeFinanceRepo())
    result = service.calculate_payouts(
        CalculatePayoutRequest(period_start=date(2026, 1, 1), period_end=date(2026, 1, 31))
    )
    assert len(result) == 1
    assert result[0].creator_share_amount == 30.0


def test_finance_mark_paid_changes_status():
    service = FinanceService(FakeFinanceRepo())
    result = service.mark_paid(1, MarkPayoutPaidRequest())
    assert result.from_status == "pending"
    assert result.to_status == "paid"
