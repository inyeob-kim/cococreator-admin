from app.core.exceptions.domain import ConflictException, NotFoundException, ValidationException
from app.modules.products.model import Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas.filters import ProductListQuery
from app.modules.products.schemas.request import (
    CreateProductRequest,
    UpdateProductPricingRequest,
    UpdateProductRequest,
)
from app.modules.products.schemas.response import ProductListResponse, ProductPricingResponse, ProductResponse


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def list_products(self, query: ProductListQuery) -> ProductListResponse:
        items, total_count = self.repository.list_products(query)
        return ProductListResponse(
            items=[self._to_response(i) for i in items],
            meta={"page": query.page, "page_size": query.page_size, "total_count": total_count},
        )

    def get_product(self, product_id: int) -> ProductResponse:
        return self._to_response(self._get_product_or_raise(product_id))

    def create_product(self, payload: CreateProductRequest) -> ProductResponse:
        if not self.repository.exists_brand(payload.brand_id):
            raise ValidationException(code="BRAND_NOT_FOUND", message="brand_id is invalid")
        self._validate_sku(payload.sku, ignore_product_id=None)

        product = Product(
            brand_id=payload.brand_id,
            product_template_id=payload.product_template_id,
            template_flavor_id=payload.template_flavor_id,
            factory_id=payload.factory_id,
            name=payload.name,
            sku=payload.sku,
            category=payload.category,
            cogs=payload.cogs,
            shipping_cost=payload.shipping_cost,
            platform_fee_rate=payload.platform_fee_rate,
            retail_price=payload.retail_price,
            currency=payload.currency.upper(),
            halal_required=payload.halal_required,
            halal_status=payload.halal_status,
            package_type=payload.package_type,
            package_size=payload.package_size,
            description=payload.description,
        )
        created = self.repository.create(product)
        return self._to_response(created)

    def update_product(self, product_id: int, payload: UpdateProductRequest) -> ProductResponse:
        product = self._get_product_or_raise(product_id)
        updates = payload.model_dump(exclude_unset=True)
        if "sku" in updates:
            self._validate_sku(updates["sku"], ignore_product_id=product.id)
        for key, value in updates.items():
            setattr(product, key, value)
        updated = self.repository.save(product)
        return self._to_response(updated)

    def update_pricing(self, product_id: int, payload: UpdateProductPricingRequest) -> ProductPricingResponse:
        product = self._get_product_or_raise(product_id)
        updates = payload.model_dump(exclude_unset=True)
        for key, value in updates.items():
            if key == "currency" and value is not None:
                setattr(product, key, value.upper())
            else:
                setattr(product, key, value)
        updated = self.repository.save(product)
        margin_rate = self._calculate_margin_rate(updated.retail_price, updated.cogs, updated.shipping_cost)
        return ProductPricingResponse(
            product_id=updated.id,
            cogs=float(updated.cogs),
            shipping_cost=float(updated.shipping_cost),
            platform_fee_rate=float(updated.platform_fee_rate),
            retail_price=float(updated.retail_price),
            currency=updated.currency,
            margin_rate=margin_rate,
        )

    def _get_product_or_raise(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise NotFoundException(message="Product not found")
        return product

    def _validate_sku(self, sku: str | None, ignore_product_id: int | None) -> None:
        if not sku:
            return
        existing = self.repository.get_by_sku(sku)
        if existing and existing.id != ignore_product_id:
            raise ConflictException(code="DUPLICATE_SKU", message="Product SKU already exists")

    @staticmethod
    def _calculate_margin_rate(retail_price: float, cogs: float, shipping_cost: float) -> float:
        if retail_price <= 0:
            return 0
        return round(((retail_price - (cogs + shipping_cost)) / retail_price) * 100, 2)

    @staticmethod
    def _to_response(product: Product) -> ProductResponse:
        return ProductResponse.model_validate(product)
