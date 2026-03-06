from datetime import datetime

from app.core.exceptions.domain import ConflictException, NotFoundException, ValidationException
from app.modules.brands.constants import ALLOWED_BRAND_STATUS_TRANSITIONS
from app.modules.brands.enums import BrandStatus
from app.modules.brands.model import Brand
from app.modules.brands.repository import BrandRepository
from app.modules.brands.schemas.filters import BrandListQuery
from app.modules.brands.schemas.request import (
    ChangeBrandStatusRequest,
    CreateBrandRequest,
    UpdateBrandRequest,
)
from app.modules.brands.schemas.response import (
    BrandListResponse,
    BrandResponse,
    BrandStatusTransitionResponse,
)


class BrandService:
    def __init__(self, repository: BrandRepository) -> None:
        self.repository = repository

    def list_brands(self, query: BrandListQuery) -> BrandListResponse:
        items, total_count = self.repository.list_brands(query)
        return BrandListResponse(
            items=[self._to_response(item) for item in items],
            meta={"page": query.page, "page_size": query.page_size, "total_count": total_count},
        )

    def get_brand(self, brand_id: int) -> BrandResponse:
        return self._to_response(self._get_brand_or_raise(brand_id))

    def create_brand(self, payload: CreateBrandRequest) -> BrandResponse:
        self._validate_creator(payload.creator_id)
        self._validate_slug_available(payload.slug, ignore_brand_id=None)

        brand = Brand(
            creator_id=payload.creator_id,
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            status=BrandStatus.PLANNING.value,
            launch_date=payload.launch_date,
            logo_url=payload.logo_url,
            brand_story=payload.brand_story,
        )
        created = self.repository.create(brand)
        return self._to_response(created)

    def update_brand(self, brand_id: int, payload: UpdateBrandRequest) -> BrandResponse:
        brand = self._get_brand_or_raise(brand_id)
        updates = payload.model_dump(exclude_unset=True)
        if "slug" in updates:
            self._validate_slug_available(updates["slug"], ignore_brand_id=brand.id)
        for key, value in updates.items():
            setattr(brand, key, value)
        updated = self.repository.save(brand)
        return self._to_response(updated)

    def change_status(
        self,
        *,
        brand_id: int,
        payload: ChangeBrandStatusRequest,
        actor_user_id: int,
    ) -> BrandStatusTransitionResponse:
        brand = self._get_brand_or_raise(brand_id)
        from_status = brand.status
        to_status = payload.to_status.value

        allowed = ALLOWED_BRAND_STATUS_TRANSITIONS.get(from_status, set())
        if to_status not in allowed:
            raise ConflictException(
                code="INVALID_STATUS_TRANSITION",
                message=f"Transition {from_status} -> {to_status} is not allowed",
            )
        if to_status == "active" and brand.launch_date is None:
            raise ValidationException(
                code="LAUNCH_DATE_REQUIRED",
                message="launch_date is required to activate a brand",
            )

        brand.status = to_status
        self.repository.save(brand)
        return BrandStatusTransitionResponse(
            brand_id=brand.id,
            from_status=from_status,
            to_status=to_status,
            reason=payload.reason,
            changed_at=datetime.utcnow(),
            changed_by_user_id=actor_user_id,
        )

    def _get_brand_or_raise(self, brand_id: int) -> Brand:
        brand = self.repository.get_by_id(brand_id)
        if brand is None:
            raise NotFoundException(message="Brand not found")
        return brand

    def _validate_creator(self, creator_id: int) -> None:
        if not self.repository.exists_creator(creator_id):
            raise ValidationException(code="CREATOR_NOT_FOUND", message="creator_id is invalid")

    def _validate_slug_available(self, slug: str | None, ignore_brand_id: int | None) -> None:
        if not slug:
            return
        existing = self.repository.get_by_slug(slug)
        if existing and existing.id != ignore_brand_id:
            raise ConflictException(code="DUPLICATE_SLUG", message="Brand slug already exists")

    @staticmethod
    def _to_response(brand: Brand) -> BrandResponse:
        return BrandResponse.model_validate(brand, from_attributes=True)
