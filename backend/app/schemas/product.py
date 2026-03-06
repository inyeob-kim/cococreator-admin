from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    brand_id: int
