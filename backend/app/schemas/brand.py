from pydantic import BaseModel


class BrandBase(BaseModel):
    name: str
