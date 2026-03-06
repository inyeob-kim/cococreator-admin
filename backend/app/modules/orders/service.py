from datetime import datetime

from app.core.exceptions.domain import ConflictException, NotFoundException, ValidationException
from app.modules.orders.constants import ALLOWED_ORDER_STATUS_TRANSITIONS
from app.modules.orders.model import Order
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas.filters import OrderListQuery
from app.modules.orders.schemas.request import ChangeOrderStatusRequest, CreateOrderRequest
from app.modules.orders.schemas.response import (
    OrderListResponse,
    OrderResponse,
    OrderStatusTransitionResponse,
    OrderSummaryResponse,
)


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def list_orders(self, query: OrderListQuery) -> OrderListResponse:
        items, total = self.repository.list_orders(query)
        return OrderListResponse(
            items=[OrderResponse.model_validate(i, from_attributes=True) for i in items],
            meta={"page": query.page, "page_size": query.page_size, "total_count": total},
        )

    def get_summary(self, query: OrderListQuery) -> OrderSummaryResponse:
        return OrderSummaryResponse(**self.repository.get_summary(query))

    def create_order(self, payload: CreateOrderRequest) -> OrderResponse:
        if not self.repository.exists_product(payload.product_id):
            raise ValidationException(code="PRODUCT_NOT_FOUND", message="product_id is invalid")
        if payload.order_number:
            existing = self.repository.get_order_by_number(payload.order_number)
            if existing:
                raise ConflictException(code="DUPLICATE_ORDER_NUMBER", message="Order number already exists")

        net_revenue = payload.net_revenue
        if net_revenue is None:
            net_revenue = payload.gross_revenue - payload.platform_fee_amount - payload.shipping_fee_amount
            if net_revenue < 0:
                net_revenue = 0

        order = Order(
            product_id=payload.product_id,
            sales_channel_id=payload.sales_channel_id,
            order_number=payload.order_number,
            order_date=payload.order_date,
            quantity=payload.quantity,
            gross_revenue=payload.gross_revenue,
            platform_fee_amount=payload.platform_fee_amount,
            shipping_fee_amount=payload.shipping_fee_amount,
            net_revenue=net_revenue,
            currency=payload.currency.upper(),
            order_status=payload.order_status.value,
            customer_country_code=payload.customer_country_code,
        )
        return OrderResponse.model_validate(self.repository.create_order(order), from_attributes=True)

    def change_status(
        self,
        *,
        order_id: int,
        payload: ChangeOrderStatusRequest,
        actor_user_id: int,
    ) -> OrderStatusTransitionResponse:
        order = self.repository.get_order(order_id)
        if order is None:
            raise NotFoundException(message="Order not found")

        from_status = order.order_status
        to_status = payload.to_status.value
        allowed = ALLOWED_ORDER_STATUS_TRANSITIONS.get(from_status, set())
        if to_status not in allowed:
            raise ConflictException(
                code="INVALID_STATUS_TRANSITION",
                message=f"Transition {from_status} -> {to_status} is not allowed",
            )

        order.order_status = to_status
        self.repository.save_order(order)
        return OrderStatusTransitionResponse(
            order_id=order.id,
            from_status=from_status,
            to_status=to_status,
            reason=payload.reason,
            changed_by_user_id=actor_user_id,
            changed_at=datetime.utcnow(),
        )
