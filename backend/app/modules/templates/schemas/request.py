from pydantic import BaseModel, Field

from app.modules.templates.enums import TemplateStatus


class CreateTemplateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    category: str = Field(min_length=1, max_length=100)
    description: str | None = None
    base_cost: float = Field(default=0, ge=0)
    suggested_price: float = Field(default=0, ge=0)
    currency: str = Field(default="USD", max_length=10)
    halal_supported: bool = False


class UpdateTemplateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    base_cost: float | None = Field(default=None, ge=0)
    suggested_price: float | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, max_length=10)
    halal_supported: bool | None = None
    status: TemplateStatus | None = None


class CreateTemplateFlavorRequest(BaseModel):
    flavor_name: str = Field(min_length=1, max_length=100)
    spice_level: str | None = Field(default=None, max_length=50)
    description: str | None = None
    additional_cost: float = Field(default=0, ge=0)


class UpdateTemplateFlavorRequest(BaseModel):
    flavor_name: str | None = Field(default=None, min_length=1, max_length=100)
    spice_level: str | None = Field(default=None, max_length=50)
    description: str | None = None
    additional_cost: float | None = Field(default=None, ge=0)
