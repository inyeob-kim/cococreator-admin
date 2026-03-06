from fastapi import FastAPI

from app.api.router import api_router
from app.core.exceptions.handlers import register_exception_handlers
from app.models.base import Base
from app.core.database import engine

# Ensure ORM models are imported so metadata includes required tables.
from app.modules.analytics import model as analytics_model  # noqa: F401
from app.modules.auth import model as auth_model  # noqa: F401
from app.modules.brands import model as brands_model  # noqa: F401
from app.modules.creators import model as creator_model  # noqa: F401
from app.modules.dashboard import model as dashboard_model  # noqa: F401
from app.modules.factories import model as factories_model  # noqa: F401
from app.modules.finance import model as finance_model  # noqa: F401
from app.modules.orders import model as orders_model  # noqa: F401
from app.modules.product_pipeline import model as pipeline_model  # noqa: F401
from app.modules.products import model as products_model  # noqa: F401
from app.modules.templates import model as templates_model  # noqa: F401


def create_app() -> FastAPI:
    app = FastAPI(title="CoCoCreator Admin API", version="0.1.0", docs_url="/docs")
    register_exception_handlers(app)
    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()
