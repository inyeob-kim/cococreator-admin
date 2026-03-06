from pydantic import BaseModel

from app.modules.product_pipeline.enums import PipelineStage


class TransitionPipelineStageRequest(BaseModel):
    to_stage: PipelineStage
    note: str | None = None
