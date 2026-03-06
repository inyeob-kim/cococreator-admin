from pydantic import BaseModel


class PipelineLogBase(BaseModel):
    product_id: int
    stage: str
