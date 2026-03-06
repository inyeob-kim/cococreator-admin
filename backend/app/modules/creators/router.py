from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.auth.enums import UserRole
from app.modules.creators.constants import CREATOR_TAG
from app.modules.creators.repository import CreatorRepository
from app.modules.creators.schemas.filters import CreatorListQuery
from app.modules.creators.schemas.request import (
    ChangeCreatorStatusRequest,
    CreateCreatorContactRequest,
    CreateCreatorRequest,
    UpdateCreatorContactRequest,
    UpdateCreatorRequest,
)
from app.modules.creators.service import CreatorService

router = APIRouter(prefix="/creators", tags=[CREATOR_TAG])


@router.get("")
def list_creators(query: CreatorListQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    service = CreatorService(CreatorRepository(db))
    result = service.list_creators(query)
    return success_response(result.model_dump())


@router.get("/{creator_id}")
def get_creator(creator_id: int, db: Session = Depends(get_db)) -> dict:
    service = CreatorService(CreatorRepository(db))
    result = service.get_creator(creator_id)
    return success_response(result.model_dump())


@router.post("", dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))])
def create_creator(payload: CreateCreatorRequest, db: Session = Depends(get_db)) -> dict:
    service = CreatorService(CreatorRepository(db))
    result = service.create_creator(payload)
    return success_response(result.model_dump(), "Creator created")


@router.patch(
    "/{creator_id}",
    dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))],
)
def update_creator(
    creator_id: int,
    payload: UpdateCreatorRequest,
    db: Session = Depends(get_db),
) -> dict:
    service = CreatorService(CreatorRepository(db))
    result = service.update_creator(creator_id, payload)
    return success_response(result.model_dump(), "Creator updated")


@router.post(
    "/{creator_id}/actions/change-status",
    dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))],
)
def change_creator_status(
    creator_id: int,
    payload: ChangeCreatorStatusRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    service = CreatorService(CreatorRepository(db))
    result = service.change_status(
        creator_id=creator_id,
        payload=payload,
        actor_user_id=current_user.id,
    )
    return success_response(result.model_dump(), "Creator status changed")


@router.get("/{creator_id}/contacts")
def list_creator_contacts(creator_id: int, db: Session = Depends(get_db)) -> dict:
    service = CreatorService(CreatorRepository(db))
    result = service.list_contacts(creator_id)
    return success_response(result.model_dump())


@router.post(
    "/{creator_id}/contacts",
    dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))],
)
def create_creator_contact(
    creator_id: int,
    payload: CreateCreatorContactRequest,
    db: Session = Depends(get_db),
) -> dict:
    service = CreatorService(CreatorRepository(db))
    result = service.create_contact(creator_id, payload)
    return success_response(result.model_dump(), "Creator contact created")


@router.patch(
    "/{creator_id}/contacts/{contact_id}",
    dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))],
)
def update_creator_contact(
    creator_id: int,
    contact_id: int,
    payload: UpdateCreatorContactRequest,
    db: Session = Depends(get_db),
) -> dict:
    service = CreatorService(CreatorRepository(db))
    result = service.update_contact(creator_id, contact_id, payload)
    return success_response(result.model_dump(), "Creator contact updated")


@router.delete(
    "/{creator_id}/contacts/{contact_id}",
    dependencies=[Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR))],
)
def delete_creator_contact(
    creator_id: int,
    contact_id: int,
    db: Session = Depends(get_db),
) -> dict:
    service = CreatorService(CreatorRepository(db))
    service.delete_contact(creator_id, contact_id)
    return success_response({"deleted": True}, "Creator contact deleted")

