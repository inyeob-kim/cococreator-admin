from datetime import datetime

from app.core.exceptions.domain import ConflictException, NotFoundException, ValidationException
from app.modules.creators.constants import ALLOWED_STATUS_TRANSITIONS, ISO_COUNTRY_CODE_LEN
from app.modules.creators.model import Creator, CreatorContact
from app.modules.creators.repository import CreatorRepository
from app.modules.creators.schemas.filters import CreatorListQuery
from app.modules.creators.schemas.request import (
    ChangeCreatorStatusRequest,
    CreateCreatorRequest,
    CreateCreatorContactRequest,
    UpdateCreatorContactRequest,
    UpdateCreatorRequest,
)
from app.modules.creators.schemas.response import (
    CreatorContactListResponse,
    CreatorContactResponse,
    CreatorListResponse,
    CreatorResponse,
    CreatorStatusTransitionResponse,
)


class CreatorService:
    def __init__(self, repository: CreatorRepository) -> None:
        self.repository = repository

    def list_creators(self, query: CreatorListQuery) -> CreatorListResponse:
        creators, total_count = self.repository.list_creators(query)
        return CreatorListResponse(
            items=[self._to_response(item) for item in creators],
            meta={
                "page": query.page,
                "page_size": query.page_size,
                "total_count": total_count,
            },
        )

    def get_creator(self, creator_id: int) -> CreatorResponse:
        creator = self.repository.get_by_id(creator_id)
        if creator is None:
            raise NotFoundException(message="Creator not found")
        return self._to_response(creator)

    def create_creator(self, payload: CreateCreatorRequest) -> CreatorResponse:
        creator = Creator(
            name=payload.name,
            display_name=payload.display_name,
            email=str(payload.email) if payload.email else None,
            phone=payload.phone,
            country_code=self._normalize_country_code(payload.country_code),
            platform=payload.platform.value if payload.platform else None,
            channel_name=payload.channel_name,
            channel_url=payload.channel_url,
            subscribers_count=payload.subscribers_count,
            avg_views=payload.avg_views,
            category=payload.category.value if payload.category else None,
            audience_summary=payload.audience_summary,
            notes=payload.notes,
        )
        created = self.repository.create(creator)
        return self._to_response(created)

    def update_creator(self, creator_id: int, payload: UpdateCreatorRequest) -> CreatorResponse:
        creator = self.repository.get_by_id(creator_id)
        if creator is None:
            raise NotFoundException(message="Creator not found")

        for field_name, field_value in payload.model_dump(exclude_unset=True).items():
            if field_name == "email" and field_value is not None:
                setattr(creator, field_name, str(field_value))
            elif field_name == "country_code":
                setattr(creator, field_name, self._normalize_country_code(field_value))
            elif field_name in {"platform", "category"} and field_value is not None:
                setattr(creator, field_name, field_value.value)
            else:
                setattr(creator, field_name, field_value)
        updated = self.repository.save(creator)
        return self._to_response(updated)

    def change_status(
        self,
        *,
        creator_id: int,
        payload: ChangeCreatorStatusRequest,
        actor_user_id: int,
    ) -> CreatorStatusTransitionResponse:
        creator = self.repository.get_by_id(creator_id)
        if creator is None:
            raise NotFoundException(message="Creator not found")

        from_status = creator.status
        to_status = payload.to_status.value
        allowed_next = ALLOWED_STATUS_TRANSITIONS.get(from_status, set())
        if to_status not in allowed_next:
            raise ConflictException(
                code="INVALID_STATUS_TRANSITION",
                message=f"Transition {from_status} -> {to_status} is not allowed",
            )

        creator.status = to_status
        self.repository.save(creator)
        return CreatorStatusTransitionResponse(
            creator_id=creator.id,
            from_status=from_status,
            to_status=to_status,
            reason=payload.reason,
            changed_at=datetime.utcnow(),
            changed_by_user_id=actor_user_id,
        )

    def list_contacts(self, creator_id: int) -> CreatorContactListResponse:
        self._get_creator_or_raise(creator_id)
        contacts = self.repository.list_contacts(creator_id)
        return CreatorContactListResponse(items=[self._to_contact_response(item) for item in contacts])

    def create_contact(
        self, creator_id: int, payload: CreateCreatorContactRequest
    ) -> CreatorContactResponse:
        self._get_creator_or_raise(creator_id)
        existing_contacts = self.repository.list_contacts(creator_id)
        is_primary = payload.is_primary or len(existing_contacts) == 0
        contact = CreatorContact(
            creator_id=creator_id,
            contact_type=payload.contact_type.value,
            contact_value=payload.contact_value,
            is_primary=is_primary,
        )
        created = self.repository.create_contact(contact)
        if is_primary:
            self._unset_primary_for_others(creator_id, keep_contact_id=created.id)
        return self._to_contact_response(created)

    def update_contact(
        self,
        creator_id: int,
        contact_id: int,
        payload: UpdateCreatorContactRequest,
    ) -> CreatorContactResponse:
        self._get_creator_or_raise(creator_id)
        contact = self.repository.get_contact(creator_id, contact_id)
        if contact is None:
            raise NotFoundException(message="Creator contact not found")

        updates = payload.model_dump(exclude_unset=True)
        if "contact_type" in updates and updates["contact_type"] is not None:
            contact.contact_type = updates["contact_type"].value
        if "contact_value" in updates and updates["contact_value"] is not None:
            contact.contact_value = updates["contact_value"]
        if "is_primary" in updates and updates["is_primary"] is not None:
            contact.is_primary = bool(updates["is_primary"])

        updated = self.repository.save_contact(contact)
        if updated.is_primary:
            self._unset_primary_for_others(creator_id, keep_contact_id=updated.id)
        else:
            self._ensure_primary_exists(creator_id)
        return self._to_contact_response(updated)

    def delete_contact(self, creator_id: int, contact_id: int) -> None:
        self._get_creator_or_raise(creator_id)
        contact = self.repository.get_contact(creator_id, contact_id)
        if contact is None:
            raise NotFoundException(message="Creator contact not found")

        self.repository.delete_contact(contact)
        self._ensure_primary_exists(creator_id)

    def _get_creator_or_raise(self, creator_id: int) -> Creator:
        creator = self.repository.get_by_id(creator_id)
        if creator is None:
            raise NotFoundException(message="Creator not found")
        return creator

    def _normalize_country_code(self, country_code: str | None) -> str | None:
        if country_code is None:
            return None
        normalized = country_code.strip().upper()
        if len(normalized) != ISO_COUNTRY_CODE_LEN:
            raise ValidationException(
                code="INVALID_COUNTRY_CODE",
                message="country_code must be a 2-letter ISO code",
            )
        return normalized

    def _unset_primary_for_others(self, creator_id: int, keep_contact_id: int) -> None:
        contacts = self.repository.list_contacts(creator_id)
        changed_items: list[CreatorContact] = []
        for item in contacts:
            if item.id != keep_contact_id and item.is_primary:
                item.is_primary = False
                changed_items.append(item)
        if changed_items:
            self.repository.save_contacts(changed_items)

    def _ensure_primary_exists(self, creator_id: int) -> None:
        contacts = self.repository.list_contacts(creator_id)
        if not contacts:
            return
        primary_count = sum(1 for item in contacts if item.is_primary)
        if primary_count == 1:
            return
        first = contacts[0]
        first.is_primary = True
        changed_items = [first]
        for item in contacts[1:]:
            if item.is_primary:
                item.is_primary = False
                changed_items.append(item)
        self.repository.save_contacts(changed_items)

    @staticmethod
    def _to_response(creator: Creator) -> CreatorResponse:
        return CreatorResponse.model_validate(creator, from_attributes=True)

    @staticmethod
    def _to_contact_response(contact: CreatorContact) -> CreatorContactResponse:
        return CreatorContactResponse.model_validate(contact, from_attributes=True)
