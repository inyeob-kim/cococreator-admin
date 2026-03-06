from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.enums import UserRole
from app.modules.finance.constants import FINANCE_TAG, PAYOUT_TAG
from app.modules.finance.repository import FinanceRepository
from app.modules.finance.schemas.request import (
    CalculatePayoutRequest,
    MarkPayoutFailedRequest,
    MarkPayoutPaidRequest,
    PayoutListQuery,
)
from app.modules.finance.service import FinanceService

router = APIRouter(tags=[FINANCE_TAG])


@router.get("/finance/summary", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.FINANCE))])
def get_finance_summary(db: Session = Depends(get_db)) -> dict:
    service = FinanceService(FinanceRepository(db))
    return success_response(service.get_summary().model_dump())


@router.get("/payouts", tags=[PAYOUT_TAG], dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.FINANCE))])
def list_payouts(query: PayoutListQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    service = FinanceService(FinanceRepository(db))
    return success_response(service.list_payouts(query).model_dump())


@router.post("/payouts/actions/calculate", tags=[PAYOUT_TAG], dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.FINANCE))])
def calculate_payouts(payload: CalculatePayoutRequest, db: Session = Depends(get_db)) -> dict:
    service = FinanceService(FinanceRepository(db))
    items = service.calculate_payouts(payload)
    return success_response({"items": [i.model_dump() for i in items]}, "Payouts calculated")


@router.post("/payouts/{payout_id}/actions/mark-paid", tags=[PAYOUT_TAG], dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.FINANCE))])
def mark_payout_paid(payout_id: int, payload: MarkPayoutPaidRequest, db: Session = Depends(get_db)) -> dict:
    service = FinanceService(FinanceRepository(db))
    return success_response(service.mark_paid(payout_id, payload).model_dump(), "Payout marked as paid")


@router.post("/payouts/{payout_id}/actions/mark-failed", tags=[PAYOUT_TAG], dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.FINANCE))])
def mark_payout_failed(payout_id: int, payload: MarkPayoutFailedRequest, db: Session = Depends(get_db)) -> dict:
    service = FinanceService(FinanceRepository(db))
    return success_response(service.mark_failed(payout_id, payload).model_dump(), "Payout marked as failed")
