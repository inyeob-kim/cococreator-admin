from app.core.exceptions.domain import NotFoundException
from app.modules.factories.model import Factory, FactoryCapability
from app.modules.factories.repository import FactoryRepository
from app.modules.factories.schemas.filters import FactoryListQuery
from app.modules.factories.schemas.request import (
    CreateFactoryCapabilityRequest,
    CreateFactoryRequest,
    UpdateFactoryCapabilityRequest,
    UpdateFactoryRequest,
)
from app.modules.factories.schemas.response import FactoryCapabilityResponse, FactoryListResponse, FactoryResponse


class FactoryService:
    def __init__(self, repository: FactoryRepository) -> None:
        self.repository = repository

    def list_factories(self, query: FactoryListQuery) -> FactoryListResponse:
        items, total = self.repository.list_factories(query)
        return FactoryListResponse(
            items=[FactoryResponse.model_validate(i) for i in items],
            meta={"page": query.page, "page_size": query.page_size, "total_count": total},
        )

    def get_factory(self, factory_id: int) -> FactoryResponse:
        return FactoryResponse.model_validate(self._get_factory_or_raise(factory_id))

    def create_factory(self, payload: CreateFactoryRequest) -> FactoryResponse:
        item = Factory(**payload.model_dump())
        if item.country_code:
            item.country_code = item.country_code.upper()
        return FactoryResponse.model_validate(self.repository.create_factory(item))

    def update_factory(self, factory_id: int, payload: UpdateFactoryRequest) -> FactoryResponse:
        item = self._get_factory_or_raise(factory_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            if key == "country_code" and value is not None:
                setattr(item, key, value.upper())
            else:
                setattr(item, key, value)
        return FactoryResponse.model_validate(self.repository.save_factory(item))

    def list_capabilities(self, factory_id: int) -> list[FactoryCapabilityResponse]:
        self._get_factory_or_raise(factory_id)
        return [FactoryCapabilityResponse.model_validate(i) for i in self.repository.list_capabilities(factory_id)]

    def create_capability(self, factory_id: int, payload: CreateFactoryCapabilityRequest) -> FactoryCapabilityResponse:
        self._get_factory_or_raise(factory_id)
        item = FactoryCapability(factory_id=factory_id, **payload.model_dump())
        item.currency = item.currency.upper()
        return FactoryCapabilityResponse.model_validate(self.repository.create_capability(item))

    def update_capability(self, factory_id: int, capability_id: int, payload: UpdateFactoryCapabilityRequest) -> FactoryCapabilityResponse:
        self._get_factory_or_raise(factory_id)
        item = self.repository.get_capability(factory_id, capability_id)
        if item is None:
            raise NotFoundException(message="Factory capability not found")
        for key, value in payload.model_dump(exclude_unset=True).items():
            if key == "currency" and value is not None:
                setattr(item, key, value.upper())
            else:
                setattr(item, key, value)
        return FactoryCapabilityResponse.model_validate(self.repository.save_capability(item))

    def delete_capability(self, factory_id: int, capability_id: int) -> None:
        self._get_factory_or_raise(factory_id)
        item = self.repository.get_capability(factory_id, capability_id)
        if item is None:
            raise NotFoundException(message="Factory capability not found")
        self.repository.delete_capability(item)

    def _get_factory_or_raise(self, factory_id: int) -> Factory:
        item = self.repository.get_factory(factory_id)
        if item is None:
            raise NotFoundException(message="Factory not found")
        return item
