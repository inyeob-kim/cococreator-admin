from datetime import datetime

from app.core.exceptions.domain import ConflictException, NotFoundException, ValidationException
from app.modules.finance.enums import PayoutStatus
from app.modules.finance.model import Payout
from app.modules.finance.repository import FinanceRepository
from app.modules.finance.schemas.request import (
    CalculatePayoutRequest,
    MarkPayoutFailedRequest,
    MarkPayoutPaidRequest,
    PayoutListQuery,
)
from app.modules.finance.schemas.response import (
    FinanceSummaryResponse,
    PayoutActionResponse,
    PayoutListResponse,
    PayoutResponse,
)


class FinanceService:
    def __init__(self, repository: FinanceRepository) -> None:
        self.repository = repository

    def get_summary(self) -> FinanceSummaryResponse:
        return FinanceSummaryResponse(**self.repository.payout_summary())

    def list_payouts(self, query: PayoutListQuery) -> PayoutListResponse:
        items, total = self.repository.list_payouts(
            creator_id=query.creator_id,
            payment_status=query.payment_status.value if query.payment_status else None,
            period_start_from=query.period_start_from,
            period_end_to=query.period_end_to,
            page=query.page,
            page_size=query.page_size,
        )
        return PayoutListResponse(
            items=[PayoutResponse.model_validate(i, from_attributes=True) for i in items],
            meta={"page": query.page, "page_size": query.page_size, "total_count": total},
        )

    def calculate_payouts(self, payload: CalculatePayoutRequest) -> list[PayoutResponse]:
        if payload.period_end < payload.period_start:
            raise ValidationException(code="INVALID_PERIOD", message="period_end must be after period_start")

        aggregates = self.repository.aggregate_revenue_by_creator(
            period_start=payload.period_start,
            period_end=payload.period_end,
            creator_id=payload.creator_id,
        )

        payouts_to_create: list[Payout] = []
        for creator_id, revenue in aggregates:
            if self.repository.has_payout_for_period(creator_id, payload.period_start, payload.period_end):
                continue
            creator_share = round(revenue * 0.3, 2)
            payouts_to_create.append(
                Payout(
                    creator_id=creator_id,
                    period_start=payload.period_start,
                    period_end=payload.period_end,
                    total_revenue=revenue,
                    creator_share_amount=creator_share,
                    currency="USD",
                    payment_status=PayoutStatus.PENDING.value,
                )
            )

        created = self.repository.create_payouts(payouts_to_create) if payouts_to_create else []
        return [PayoutResponse.model_validate(i, from_attributes=True) for i in created]

    def mark_paid(self, payout_id: int, payload: MarkPayoutPaidRequest) -> PayoutActionResponse:
        payout = self._get_payout_or_raise(payout_id)
        if payout.payment_status != PayoutStatus.PENDING.value:
            raise ConflictException(code="INVALID_PAYOUT_STATUS", message="Only pending payouts can be marked as paid")

        from_status = payout.payment_status
        payout.payment_status = PayoutStatus.PAID.value
        payout.paid_at = payload.paid_at or datetime.utcnow()
        self.repository.save_payout(payout)
        return PayoutActionResponse(
            payout_id=payout.id,
            from_status=from_status,
            to_status=payout.payment_status,
            changed_at=datetime.utcnow(),
        )

    def mark_failed(self, payout_id: int, _: MarkPayoutFailedRequest) -> PayoutActionResponse:
        payout = self._get_payout_or_raise(payout_id)
        if payout.payment_status != PayoutStatus.PENDING.value:
            raise ConflictException(code="INVALID_PAYOUT_STATUS", message="Only pending payouts can be marked as failed")

        from_status = payout.payment_status
        payout.payment_status = PayoutStatus.FAILED.value
        self.repository.save_payout(payout)
        return PayoutActionResponse(
            payout_id=payout.id,
            from_status=from_status,
            to_status=payout.payment_status,
            changed_at=datetime.utcnow(),
        )

    def _get_payout_or_raise(self, payout_id: int) -> Payout:
        payout = self.repository.get_payout(payout_id)
        if payout is None:
            raise NotFoundException(message="Payout not found")
        return payout
