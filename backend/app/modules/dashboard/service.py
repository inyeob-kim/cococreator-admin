from app.modules.dashboard.repository import DashboardRepository
from app.modules.dashboard.schemas.response import (
    CreatorPipelineCountResponse,
    DashboardSummaryResponse,
    TopProductResponse,
)


class DashboardService:
    def __init__(self, repository: DashboardRepository) -> None:
        self.repository = repository

    def get_summary(self) -> DashboardSummaryResponse:
        return DashboardSummaryResponse(**self.repository.summary())

    def get_creator_pipeline(self) -> list[CreatorPipelineCountResponse]:
        return [CreatorPipelineCountResponse(**item) for item in self.repository.creator_pipeline_counts()]

    def get_top_products(self, limit: int = 5) -> list[TopProductResponse]:
        return [TopProductResponse(**item) for item in self.repository.top_products(limit)]
