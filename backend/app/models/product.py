from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    brand_id: int
