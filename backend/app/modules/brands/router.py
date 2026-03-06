from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.auth.enums import UserRole
from app.modules.brands.constants import BRAND_TAG
from app.modules.brands.repository import BrandRepository
from app.modules.brands.schemas.filters import BrandListQuery
from app.modules.brands.schemas.request import ChangeBrandStatusRequest, CreateBrandRequest, UpdateBrandRequest
from app.modules.brands.service import BrandService

router = APIRouter(prefix="/brands", tags=[BRAND_TAG])


@router.get("")
def list_brands(query: BrandListQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    service = BrandService(BrandRepository(db))
    return success_response(service.list_brands(query).model_dump())


@router.get("/{brand_id}")
def get_brand(brand_id: int, db: Session = Depends(get_db)) -> dict:
    service = BrandService(BrandRepository(db))
    return success_response(service.get_brand(brand_id).model_dump())


@router.post("", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def create_brand(payload: CreateBrandRequest, db: Session = Depends(get_db)) -> dict:
    service = BrandService(BrandRepository(db))
    return success_response(service.create_brand(payload).model_dump(), "Brand created")


@router.patch("/{brand_id}", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def update_brand(brand_id: int, payload: UpdateBrandRequest, db: Session = Depends(get_db)) -> dict:
    service = BrandService(BrandRepository(db))
    return success_response(service.update_brand(brand_id, payload).model_dump(), "Brand updated")


@router.post("/{brand_id}/actions/change-status", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def change_brand_status(
    brand_id: int,
    payload: ChangeBrandStatusRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    service = BrandService(BrandRepository(db))
    result = service.change_status(brand_id=brand_id, payload=payload, actor_user_id=current_user.id)
    return success_response(result.model_dump(), "Brand status changed")
