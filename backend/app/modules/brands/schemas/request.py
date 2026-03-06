from datetime import date

from pydantic import BaseModel, Field

from app.modules.brands.enums import BrandStatus


class CreateBrandRequest(BaseModel):
    creator_id: int
    name: str = Field(min_length=1, max_length=150)
    slug: str | None = Field(default=None, max_length=150)
    description: str | None = None
    launch_date: date | None = None
    logo_url: str | None = None
    brand_story: str | None = None


class UpdateBrandRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    slug: str | None = Field(default=None, max_length=150)
    description: str | None = None
    launch_date: date | None = None
    logo_url: str | None = None
    brand_story: str | None = None


class ChangeBrandStatusRequest(BaseModel):
    to_status: BrandStatus
    reason: str | None = None
