from pydantic import BaseModel


class TrendPointResponse(BaseModel):
    bucket: str
    value: float


class TopCreatorResponse(BaseModel):
    creator_id: int
    creator_name: str
    revenue: float


class TopProductResponse(BaseModel):
    product_id: int
    product_name: str
    sales: int
    revenue: float
