from app.modules.creators.schemas.request import (
    ChangeCreatorStatusRequest,
    CreateCreatorContactRequest,
    CreateCreatorRequest,
)
from app.modules.creators.service import CreatorService
from app.modules.creators.enums import CreatorContactType, CreatorStatus
from app.core.exceptions.domain import ConflictException


class _Creator:
    def __init__(self, creator_id: int, status: str = "lead"):
        self.id = creator_id
        self.name = "Creator"
        self.display_name = None
        self.email = None
        self.phone = None
        self.country_code = None
        self.platform = None
        self.channel_name = None
        self.channel_url = None
        self.subscribers_count = 0
        self.avg_views = 0
        self.category = None
        self.status = status
        self.audience_summary = None
        self.notes = None
        self.created_at = __import__("datetime").datetime.utcnow()
        self.updated_at = __import__("datetime").datetime.utcnow()


class _Contact:
    def __init__(self, contact_id: int, creator_id: int, is_primary: bool):
        self.id = contact_id
        self.creator_id = creator_id
        self.contact_type = "email"
        self.contact_value = "a@test.com"
        self.is_primary = is_primary
        self.created_at = __import__("datetime").datetime.utcnow()
        self.updated_at = __import__("datetime").datetime.utcnow()


class FakeCreatorRepo:
    def __init__(self):
        self.creator = _Creator(1)
        self.contacts = []
        self._next_contact_id = 1

    def list_creators(self, query):
        return [self.creator], 1

    def get_by_id(self, creator_id):
        return self.creator if creator_id == self.creator.id else None

    def create(self, creator):
        creator.id = self.creator.id
        creator.created_at = self.creator.created_at
        creator.updated_at = self.creator.updated_at
        self.creator = creator
        return creator

    def save(self, creator):
        self.creator = creator
        return creator

    def list_contacts(self, creator_id):
        return [c for c in self.contacts if c.creator_id == creator_id]

    def get_contact(self, creator_id, contact_id):
        for contact in self.contacts:
            if contact.creator_id == creator_id and contact.id == contact_id:
                return contact
        return None

    def create_contact(self, contact):
        contact.id = self._next_contact_id
        contact.created_at = __import__("datetime").datetime.utcnow()
        contact.updated_at = __import__("datetime").datetime.utcnow()
        self._next_contact_id += 1
        self.contacts.append(contact)
        return contact

    def save_contact(self, contact):
        contact.updated_at = __import__("datetime").datetime.utcnow()
        return contact

    def save_contacts(self, contacts):
        for contact in contacts:
            self.save_contact(contact)

    def delete_contact(self, contact):
        self.contacts = [c for c in self.contacts if c.id != contact.id]


def test_creator_status_transition_rejects_invalid_path():
    repo = FakeCreatorRepo()
    service = CreatorService(repo)

    try:
        service.change_status(
            creator_id=1,
            payload=ChangeCreatorStatusRequest(to_status=CreatorStatus.PARTNER),
            actor_user_id=10,
        )
        assert False, "Expected ConflictException"
    except ConflictException:
        assert True


def test_creator_contact_primary_rule_keeps_single_primary():
    repo = FakeCreatorRepo()
    service = CreatorService(repo)

    c1 = service.create_contact(1, CreateCreatorContactRequest(contact_type=CreatorContactType.EMAIL, contact_value="a@test.com", is_primary=False))
    c2 = service.create_contact(1, CreateCreatorContactRequest(contact_type=CreatorContactType.MANAGER, contact_value="b@test.com", is_primary=True))

    assert c1.is_primary is True
    assert c2.is_primary is True

    contacts = service.list_contacts(1).items
    primary_count = len([c for c in contacts if c.is_primary])
    assert primary_count == 1
