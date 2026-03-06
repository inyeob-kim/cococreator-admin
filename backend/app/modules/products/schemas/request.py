from pydantic import BaseModel, Field


class CreateProductRequest(BaseModel):
    brand_id: int
    product_template_id: int | None = None
    template_flavor_id: int | None = None
    factory_id: int | None = None
    name: str = Field(min_length=1, max_length=150)
    sku: str | None = Field(default=None, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    cogs: float = Field(default=0, ge=0)
    shipping_cost: float = Field(default=0, ge=0)
    platform_fee_rate: float = Field(default=0, ge=0)
    retail_price: float = Field(default=0, ge=0)
    currency: str = Field(default="USD", max_length=10)
    halal_required: bool = False
    halal_status: str | None = "not_started"
    package_type: str | None = Field(default=None, max_length=100)
    package_size: str | None = Field(default=None, max_length=100)
    description: str | None = None


class UpdateProductRequest(BaseModel):
    product_template_id: int | None = None
    template_flavor_id: int | None = None
    factory_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=150)
    sku: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    halal_required: bool | None = None
    halal_status: str | None = None
    package_type: str | None = Field(default=None, max_length=100)
    package_size: str | None = Field(default=None, max_length=100)
    description: str | None = None


class UpdateProductPricingRequest(BaseModel):
    cogs: float | None = Field(default=None, ge=0)
    shipping_cost: float | None = Field(default=None, ge=0)
    platform_fee_rate: float | None = Field(default=None, ge=0)
    retail_price: float | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, max_length=10)
