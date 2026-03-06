from app.modules.analytics.repository import AnalyticsRepository
from app.modules.analytics.schemas.response import TopCreatorResponse, TopProductResponse, TrendPointResponse


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository) -> None:
        self.repository = repository

    def revenue_trend(self) -> list[TrendPointResponse]:
        return [TrendPointResponse(**item) for item in self.repository.revenue_trend()]

    def order_trend(self) -> list[TrendPointResponse]:
        return [TrendPointResponse(**item) for item in self.repository.order_trend()]

    def top_creators(self, limit: int) -> list[TopCreatorResponse]:
        return [TopCreatorResponse(**item) for item in self.repository.top_creators(limit)]

    def top_products(self, limit: int) -> list[TopProductResponse]:
        return [TopProductResponse(**item) for item in self.repository.top_products(limit)]
