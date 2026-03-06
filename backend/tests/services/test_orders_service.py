from datetime import datetime

from app.modules.orders.schemas.request import ChangeOrderStatusRequest, CreateOrderRequest
from app.modules.orders.service import OrderService
from app.modules.orders.enums import OrderStatus


class _Order:
    def __init__(self):
        self.id = 1
        self.product_id = 1
        self.sales_channel_id = None
        self.order_number = "ORD-1"
        self.order_date = datetime.utcnow()
        self.quantity = 1
        self.gross_revenue = 100.0
        self.platform_fee_amount = 10.0
        self.shipping_fee_amount = 5.0
        self.net_revenue = 85.0
        self.currency = "USD"
        self.order_status = "paid"
        self.customer_country_code = None
        self.created_at = datetime.utcnow()


class FakeOrderRepo:
    def __init__(self):
        self.order = _Order()

    def list_orders(self, query):
        return [self.order], 1

    def get_order(self, order_id):
        return self.order if order_id == 1 else None

    def get_order_by_number(self, number):
        return self.order if number == self.order.order_number else None

    def exists_product(self, product_id):
        return product_id == 1

    def create_order(self, order):
        order.id = 2
        order.created_at = datetime.utcnow()
        self.order = order
        return order

    def save_order(self, order):
        self.order = order
        return order

    def get_summary(self, query):
        return {
            "total_orders": 1,
            "total_quantity": 1,
            "total_gross_revenue": 100.0,
            "total_platform_fee": 10.0,
            "total_shipping_fee": 5.0,
            "total_net_revenue": 85.0,
        }


def test_order_create_calculates_net_revenue_when_missing():
    service = OrderService(FakeOrderRepo())
    result = service.create_order(
        CreateOrderRequest(
            product_id=1,
            order_number="ORD-2",
            order_date=datetime.utcnow(),
            quantity=1,
            gross_revenue=100,
            platform_fee_amount=10,
            shipping_fee_amount=5,
            net_revenue=None,
            currency="USD",
            order_status=OrderStatus.PAID,
        )
    )
    assert result.net_revenue == 85.0


def test_order_status_transition_paid_to_shipped():
    service = OrderService(FakeOrderRepo())
    result = service.change_status(
        order_id=1,
        payload=ChangeOrderStatusRequest(to_status=OrderStatus.SHIPPED),
        actor_user_id=1,
    )
    assert result.from_status == "paid"
    assert result.to_status == "shipped"
