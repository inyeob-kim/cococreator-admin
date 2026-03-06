from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.enums import UserRole
from app.modules.templates.constants import TEMPLATE_TAG
from app.modules.templates.repository import TemplateRepository
from app.modules.templates.schemas.filters import TemplateListQuery
from app.modules.templates.schemas.request import (
    CreateTemplateFlavorRequest,
    CreateTemplateRequest,
    UpdateTemplateFlavorRequest,
    UpdateTemplateRequest,
)
from app.modules.templates.service import TemplateService

router = APIRouter(prefix="/templates", tags=[TEMPLATE_TAG])


@router.get("")
def list_templates(query: TemplateListQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    service = TemplateService(TemplateRepository(db))
    return success_response(service.list_templates(query).model_dump())


@router.get("/{template_id}")
def get_template(template_id: int, db: Session = Depends(get_db)) -> dict:
    service = TemplateService(TemplateRepository(db))
    return success_response(service.get_template(template_id).model_dump())


@router.post("", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def create_template(payload: CreateTemplateRequest, db: Session = Depends(get_db)) -> dict:
    service = TemplateService(TemplateRepository(db))
    return success_response(service.create_template(payload).model_dump(), "Template created")


@router.patch("/{template_id}", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def update_template(template_id: int, payload: UpdateTemplateRequest, db: Session = Depends(get_db)) -> dict:
    service = TemplateService(TemplateRepository(db))
    return success_response(service.update_template(template_id, payload).model_dump(), "Template updated")


@router.get("/{template_id}/flavors")
def list_flavors(template_id: int, db: Session = Depends(get_db)) -> dict:
    service = TemplateService(TemplateRepository(db))
    return success_response({"items": [i.model_dump() for i in service.list_flavors(template_id)]})


@router.post("/{template_id}/flavors", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def create_flavor(template_id: int, payload: CreateTemplateFlavorRequest, db: Session = Depends(get_db)) -> dict:
    service = TemplateService(TemplateRepository(db))
    return success_response(service.create_flavor(template_id, payload).model_dump(), "Template flavor created")


@router.patch("/{template_id}/flavors/{flavor_id}", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def update_flavor(template_id: int, flavor_id: int, payload: UpdateTemplateFlavorRequest, db: Session = Depends(get_db)) -> dict:
    service = TemplateService(TemplateRepository(db))
    return success_response(service.update_flavor(template_id, flavor_id, payload).model_dump(), "Template flavor updated")


@router.delete("/{template_id}/flavors/{flavor_id}", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def delete_flavor(template_id: int, flavor_id: int, db: Session = Depends(get_db)) -> dict:
    service = TemplateService(TemplateRepository(db))
    service.delete_flavor(template_id, flavor_id)
    return success_response({"deleted": True}, "Template flavor deleted")
