from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.enums import UserRole
from app.modules.products.constants import PRODUCT_TAG
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas.filters import ProductListQuery
from app.modules.products.schemas.request import (
    CreateProductRequest,
    UpdateProductPricingRequest,
    UpdateProductRequest,
)
from app.modules.products.service import ProductService

router = APIRouter(prefix="/products", tags=[PRODUCT_TAG])


@router.get("")
def list_products(query: ProductListQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    service = ProductService(ProductRepository(db))
    return success_response(service.list_products(query).model_dump())


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)) -> dict:
    service = ProductService(ProductRepository(db))
    return success_response(service.get_product(product_id).model_dump())


@router.post("", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def create_product(payload: CreateProductRequest, db: Session = Depends(get_db)) -> dict:
    service = ProductService(ProductRepository(db))
    return success_response(service.create_product(payload).model_dump(), "Product created")


@router.patch("/{product_id}", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def update_product(product_id: int, payload: UpdateProductRequest, db: Session = Depends(get_db)) -> dict:
    service = ProductService(ProductRepository(db))
    return success_response(service.update_product(product_id, payload).model_dump(), "Product updated")


@router.post("/{product_id}/actions/update-pricing", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def update_product_pricing(
    product_id: int,
    payload: UpdateProductPricingRequest,
    db: Session = Depends(get_db),
) -> dict:
    service = ProductService(ProductRepository(db))
    return success_response(service.update_pricing(product_id, payload).model_dump(), "Product pricing updated")
