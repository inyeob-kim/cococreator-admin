from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.auth.enums import UserRole
from app.modules.product_pipeline.constants import PIPELINE_TAG
from app.modules.product_pipeline.repository import ProductPipelineRepository
from app.modules.product_pipeline.schemas.request import TransitionPipelineStageRequest
from app.modules.product_pipeline.service import ProductPipelineService

router = APIRouter(prefix="/product-pipeline", tags=[PIPELINE_TAG])


@router.get("/board")
def get_pipeline_board(db: Session = Depends(get_db)) -> dict:
    service = ProductPipelineService(ProductPipelineRepository(db))
    return success_response(service.get_board().model_dump())


@router.post("/products/{product_id}/actions/transition-stage", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def transition_pipeline_stage(
    product_id: int,
    payload: TransitionPipelineStageRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    service = ProductPipelineService(ProductPipelineRepository(db))
    result = service.transition_stage(product_id=product_id, payload=payload, actor_user_id=current_user.id)
    return success_response(result.model_dump(), "Pipeline stage transitioned")


@router.get("/products/{product_id}/logs")
def get_pipeline_logs(product_id: int, db: Session = Depends(get_db)) -> dict:
    service = ProductPipelineService(ProductPipelineRepository(db))
    return success_response({"items": [i.model_dump() for i in service.get_logs(product_id)]})
