from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.auth.enums import UserRole
from app.modules.orders.constants import ORDER_TAG
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas.filters import OrderListQuery
from app.modules.orders.schemas.request import ChangeOrderStatusRequest, CreateOrderRequest
from app.modules.orders.service import OrderService

router = APIRouter(prefix="/orders", tags=[ORDER_TAG])


@router.get("")
def list_orders(query: OrderListQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    service = OrderService(OrderRepository(db))
    return success_response(service.list_orders(query).model_dump())


@router.get("/summary")
def get_order_summary(query: OrderListQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    service = OrderService(OrderRepository(db))
    return success_response(service.get_summary(query).model_dump())


@router.post("", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def create_order(payload: CreateOrderRequest, db: Session = Depends(get_db)) -> dict:
    service = OrderService(OrderRepository(db))
    return success_response(service.create_order(payload).model_dump(), "Order created")


@router.post("/{order_id}/actions/change-status", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR, UserRole.FINANCE))])
def change_order_status(
    order_id: int,
    payload: ChangeOrderStatusRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    service = OrderService(OrderRepository(db))
    result = service.change_status(order_id=order_id, payload=payload, actor_user_id=current_user.id)
    return success_response(result.model_dump(), "Order status changed")
