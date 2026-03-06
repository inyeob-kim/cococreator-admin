from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.enums import UserRole
from app.modules.factories.constants import FACTORY_TAG
from app.modules.factories.repository import FactoryRepository
from app.modules.factories.schemas.filters import FactoryListQuery
from app.modules.factories.schemas.request import (
    CreateFactoryCapabilityRequest,
    CreateFactoryRequest,
    UpdateFactoryCapabilityRequest,
    UpdateFactoryRequest,
)
from app.modules.factories.service import FactoryService

router = APIRouter(prefix="/factories", tags=[FACTORY_TAG])


@router.get("")
def list_factories(query: FactoryListQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    service = FactoryService(FactoryRepository(db))
    return success_response(service.list_factories(query).model_dump())


@router.get("/{factory_id}")
def get_factory(factory_id: int, db: Session = Depends(get_db)) -> dict:
    service = FactoryService(FactoryRepository(db))
    return success_response(service.get_factory(factory_id).model_dump())


@router.post("", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def create_factory(payload: CreateFactoryRequest, db: Session = Depends(get_db)) -> dict:
    service = FactoryService(FactoryRepository(db))
    return success_response(service.create_factory(payload).model_dump(), "Factory created")


@router.patch("/{factory_id}", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def update_factory(factory_id: int, payload: UpdateFactoryRequest, db: Session = Depends(get_db)) -> dict:
    service = FactoryService(FactoryRepository(db))
    return success_response(service.update_factory(factory_id, payload).model_dump(), "Factory updated")


@router.get("/{factory_id}/capabilities")
def list_capabilities(factory_id: int, db: Session = Depends(get_db)) -> dict:
    service = FactoryService(FactoryRepository(db))
    return success_response({"items": [i.model_dump() for i in service.list_capabilities(factory_id)]})


@router.post("/{factory_id}/capabilities", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def create_capability(factory_id: int, payload: CreateFactoryCapabilityRequest, db: Session = Depends(get_db)) -> dict:
    service = FactoryService(FactoryRepository(db))
    return success_response(service.create_capability(factory_id, payload).model_dump(), "Factory capability created")


@router.patch("/{factory_id}/capabilities/{capability_id}", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def update_capability(
    factory_id: int,
    capability_id: int,
    payload: UpdateFactoryCapabilityRequest,
    db: Session = Depends(get_db),
) -> dict:
    service = FactoryService(FactoryRepository(db))
    return success_response(service.update_capability(factory_id, capability_id, payload).model_dump(), "Factory capability updated")


@router.delete("/{factory_id}/capabilities/{capability_id}", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def delete_capability(factory_id: int, capability_id: int, db: Session = Depends(get_db)) -> dict:
    service = FactoryService(FactoryRepository(db))
    service.delete_capability(factory_id, capability_id)
    return success_response({"deleted": True}, "Factory capability deleted")
