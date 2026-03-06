from datetime import datetime

from app.core.exceptions.domain import ConflictException, NotFoundException
from app.modules.product_pipeline.constants import PIPELINE_STAGE_ORDER
from app.modules.product_pipeline.model import ProductPipelineLog
from app.modules.product_pipeline.repository import ProductPipelineRepository
from app.modules.product_pipeline.schemas.request import TransitionPipelineStageRequest
from app.modules.product_pipeline.schemas.response import (
    PipelineBoardColumn,
    PipelineBoardProductItem,
    PipelineBoardResponse,
    PipelineLogResponse,
    PipelineTransitionResponse,
)


class ProductPipelineService:
    def __init__(self, repository: ProductPipelineRepository) -> None:
        self.repository = repository

    def get_board(self) -> PipelineBoardResponse:
        products = self.repository.list_products()
        columns: list[PipelineBoardColumn] = []
        for stage in PIPELINE_STAGE_ORDER:
            stage_products = [p for p in products if p.status == stage]
            columns.append(
                PipelineBoardColumn(
                    stage=stage,
                    count=len(stage_products),
                    products=[
                        PipelineBoardProductItem(
                            id=p.id,
                            name=p.name,
                            brand_id=p.brand_id,
                            stage=p.status,
                        )
                        for p in stage_products
                    ],
                )
            )
        return PipelineBoardResponse(columns=columns)

    def transition_stage(
        self,
        *,
        product_id: int,
        payload: TransitionPipelineStageRequest,
        actor_user_id: int,
    ) -> PipelineTransitionResponse:
        product = self.repository.get_product(product_id)
        if product is None:
            raise NotFoundException(message="Product not found")

        from_stage = product.status
        to_stage = payload.to_stage.value
        if from_stage == to_stage:
            raise ConflictException(code="NO_STAGE_CHANGE", message="Stage is unchanged")

        if not self._is_forward_transition(from_stage, to_stage):
            raise ConflictException(
                code="INVALID_STAGE_TRANSITION",
                message=f"Transition {from_stage} -> {to_stage} is not allowed",
            )

        product.status = to_stage
        self.repository.save_product(product)
        log = ProductPipelineLog(
            product_id=product.id,
            stage=to_stage,
            note=payload.note,
            changed_by_user_id=actor_user_id,
        )
        self.repository.create_log(log)

        return PipelineTransitionResponse(
            product_id=product.id,
            from_stage=from_stage,
            to_stage=to_stage,
            note=payload.note,
            changed_by_user_id=actor_user_id,
            changed_at=datetime.utcnow(),
        )

    def get_logs(self, product_id: int) -> list[PipelineLogResponse]:
        product = self.repository.get_product(product_id)
        if product is None:
            raise NotFoundException(message="Product not found")
        logs = self.repository.list_logs(product_id)
        return [PipelineLogResponse.model_validate(log) for log in logs]

    @staticmethod
    def _is_forward_transition(from_stage: str, to_stage: str) -> bool:
        if from_stage not in PIPELINE_STAGE_ORDER or to_stage not in PIPELINE_STAGE_ORDER:
            return False
        return PIPELINE_STAGE_ORDER.index(to_stage) > PIPELINE_STAGE_ORDER.index(from_stage)
