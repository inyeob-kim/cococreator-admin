from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.brands import router as brands_router
from app.api.v1.creators import router as creators_router
from app.api.v1.factories import router as factories_router
from app.api.v1.finance import router as finance_router
from app.api.v1.notes import router as notes_router
from app.api.v1.orders import router as orders_router
from app.api.v1.pipeline import router as pipeline_router
from app.api.v1.products import router as products_router
from app.api.v1.templates import router as templates_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(creators_router)
api_router.include_router(brands_router)
api_router.include_router(products_router)
api_router.include_router(templates_router)
api_router.include_router(factories_router)
api_router.include_router(pipeline_router)
api_router.include_router(orders_router)
api_router.include_router(finance_router)
api_router.include_router(notes_router)