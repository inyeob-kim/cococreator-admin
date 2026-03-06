from datetime import datetime

from pydantic import BaseModel


class PipelineBoardProductItem(BaseModel):
    id: int
    name: str
    brand_id: int
    stage: str


class PipelineBoardColumn(BaseModel):
    stage: str
    count: int
    products: list[PipelineBoardProductItem]


class PipelineBoardResponse(BaseModel):
    columns: list[PipelineBoardColumn]


class PipelineTransitionResponse(BaseModel):
    product_id: int
    from_stage: str
    to_stage: str
    note: str | None
    changed_by_user_id: int
    changed_at: datetime


class PipelineLogResponse(BaseModel):
    id: int
    product_id: int
    stage: str
    note: str | None
    changed_by_user_id: int | None
    created_at: datetime
    updated_at: datetime
