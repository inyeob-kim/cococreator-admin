from fastapi import APIRouter

from app.api.health import router as health_router
from app.modules.analytics.router import router as analytics_router
from app.modules.auth.router import router as auth_router
from app.modules.brands.router import router as brands_router
from app.modules.creators.router import router as creators_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.factories.router import router as factories_router
from app.modules.finance.router import router as finance_router
from app.modules.orders.router import router as orders_router
from app.modules.product_pipeline.router import router as product_pipeline_router
from app.modules.products.router import router as products_router
from app.modules.templates.router import router as templates_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(creators_router)
api_router.include_router(brands_router)
api_router.include_router(products_router)
api_router.include_router(product_pipeline_router)
api_router.include_router(dashboard_router)
api_router.include_router(templates_router)
api_router.include_router(factories_router)
api_router.include_router(orders_router)
api_router.include_router(finance_router)
api_router.include_router(analytics_router)