from app.core.exceptions.domain import NotFoundException
from app.modules.templates.model import ProductTemplate, TemplateFlavor
from app.modules.templates.repository import TemplateRepository
from app.modules.templates.schemas.filters import TemplateListQuery
from app.modules.templates.schemas.request import (
    CreateTemplateFlavorRequest,
    CreateTemplateRequest,
    UpdateTemplateFlavorRequest,
    UpdateTemplateRequest,
)
from app.modules.templates.schemas.response import (
    TemplateFlavorResponse,
    TemplateListResponse,
    TemplateResponse,
)


class TemplateService:
    def __init__(self, repository: TemplateRepository) -> None:
        self.repository = repository

    def list_templates(self, query: TemplateListQuery) -> TemplateListResponse:
        items, total = self.repository.list_templates(query)
        return TemplateListResponse(
            items=[TemplateResponse.model_validate(i) for i in items],
            meta={"page": query.page, "page_size": query.page_size, "total_count": total},
        )

    def get_template(self, template_id: int) -> TemplateResponse:
        template = self.repository.get_template(template_id)
        if template is None:
            raise NotFoundException(message="Template not found")
        return TemplateResponse.model_validate(template)

    def create_template(self, payload: CreateTemplateRequest) -> TemplateResponse:
        item = ProductTemplate(
            name=payload.name,
            category=payload.category,
            description=payload.description,
            base_cost=payload.base_cost,
            suggested_price=payload.suggested_price,
            currency=payload.currency.upper(),
            halal_supported=payload.halal_supported,
        )
        return TemplateResponse.model_validate(self.repository.create_template(item))

    def update_template(self, template_id: int, payload: UpdateTemplateRequest) -> TemplateResponse:
        template = self.repository.get_template(template_id)
        if template is None:
            raise NotFoundException(message="Template not found")
        updates = payload.model_dump(exclude_unset=True)
        for key, value in updates.items():
            if key == "status" and value is not None:
                setattr(template, key, value.value)
            elif key == "currency" and value is not None:
                setattr(template, key, value.upper())
            else:
                setattr(template, key, value)
        return TemplateResponse.model_validate(self.repository.save_template(template))

    def list_flavors(self, template_id: int) -> list[TemplateFlavorResponse]:
        self._get_template_or_raise(template_id)
        return [TemplateFlavorResponse.model_validate(i) for i in self.repository.list_flavors(template_id)]

    def create_flavor(self, template_id: int, payload: CreateTemplateFlavorRequest) -> TemplateFlavorResponse:
        self._get_template_or_raise(template_id)
        item = TemplateFlavor(
            product_template_id=template_id,
            flavor_name=payload.flavor_name,
            spice_level=payload.spice_level,
            description=payload.description,
            additional_cost=payload.additional_cost,
        )
        return TemplateFlavorResponse.model_validate(self.repository.create_flavor(item))

    def update_flavor(self, template_id: int, flavor_id: int, payload: UpdateTemplateFlavorRequest) -> TemplateFlavorResponse:
        self._get_template_or_raise(template_id)
        flavor = self.repository.get_flavor(template_id, flavor_id)
        if flavor is None:
            raise NotFoundException(message="Template flavor not found")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(flavor, key, value)
        return TemplateFlavorResponse.model_validate(self.repository.save_flavor(flavor))

    def delete_flavor(self, template_id: int, flavor_id: int) -> None:
        self._get_template_or_raise(template_id)
        flavor = self.repository.get_flavor(template_id, flavor_id)
        if flavor is None:
            raise NotFoundException(message="Template flavor not found")
        self.repository.delete_flavor(flavor)

    def _get_template_or_raise(self, template_id: int) -> ProductTemplate:
        item = self.repository.get_template(template_id)
        if item is None:
            raise NotFoundException(message="Template not found")
        return item
