from app.modules.brands.schemas.request import ChangeBrandStatusRequest, CreateBrandRequest
from app.modules.brands.service import BrandService
from app.modules.brands.enums import BrandStatus
from app.core.exceptions.domain import ValidationException


class _Brand:
    def __init__(self):
        self.id = 1
        self.creator_id = 1
        self.name = "Brand"
        self.slug = "brand"
        self.description = None
        self.status = "planning"
        self.launch_date = None
        self.logo_url = None
        self.brand_story = None
        self.created_at = __import__("datetime").datetime.utcnow()
        self.updated_at = __import__("datetime").datetime.utcnow()


class FakeBrandRepo:
    def __init__(self):
        self.brand = _Brand()

    def list_brands(self, query):
        return [self.brand], 1

    def get_by_id(self, brand_id):
        return self.brand if brand_id == 1 else None

    def exists_creator(self, creator_id):
        return creator_id == 1

    def get_by_slug(self, slug):
        return None

    def create(self, brand):
        brand.id = 1
        brand.created_at = self.brand.created_at
        brand.updated_at = self.brand.updated_at
        self.brand = brand
        return brand

    def save(self, brand):
        self.brand = brand
        return brand


def test_brand_activation_requires_launch_date():
    service = BrandService(FakeBrandRepo())
    service.create_brand(CreateBrandRequest(creator_id=1, name="B", slug="b"))

    try:
        service.change_status(
            brand_id=1,
            payload=ChangeBrandStatusRequest(to_status=BrandStatus.ACTIVE),
            actor_user_id=1,
        )
        assert False, "Expected ValidationException"
    except ValidationException:
        assert True
