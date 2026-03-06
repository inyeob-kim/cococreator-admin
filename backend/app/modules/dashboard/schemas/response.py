from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_creators: int
    active_brands: int
    launched_products: int
    total_revenue: float


class CreatorPipelineCountResponse(BaseModel):
    status: str
    count: int


class TopProductResponse(BaseModel):
    product_id: int
    product_name: str
    orders: int
    revenue: float
    margin_rate: float
