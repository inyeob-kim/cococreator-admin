from pydantic import BaseModel, Field


class CreateFactoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    website_url: str | None = None
    contact_name: str | None = Field(default=None, max_length=100)
    contact_email: str | None = Field(default=None, max_length=255)
    contact_phone: str | None = Field(default=None, max_length=50)
    halal_certified: bool = False
    notes: str | None = None


class UpdateFactoryRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    website_url: str | None = None
    contact_name: str | None = Field(default=None, max_length=100)
    contact_email: str | None = Field(default=None, max_length=255)
    contact_phone: str | None = Field(default=None, max_length=50)
    halal_certified: bool | None = None
    notes: str | None = None


class CreateFactoryCapabilityRequest(BaseModel):
    category: str = Field(min_length=1, max_length=100)
    moq: int | None = Field(default=None, ge=1)
    lead_time_days: int | None = Field(default=None, ge=1)
    estimated_unit_cost: float | None = Field(default=None, ge=0)
    currency: str = Field(default="USD", max_length=10)
    notes: str | None = None


class UpdateFactoryCapabilityRequest(BaseModel):
    category: str | None = Field(default=None, min_length=1, max_length=100)
    moq: int | None = Field(default=None, ge=1)
    lead_time_days: int | None = Field(default=None, ge=1)
    estimated_unit_cost: float | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, max_length=10)
    notes: str | None = None
