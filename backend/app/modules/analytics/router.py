from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.analytics.constants import ANALYTICS_TAG
from app.modules.analytics.repository import AnalyticsRepository
from app.modules.analytics.service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=[ANALYTICS_TAG])


@router.get("/revenue-trend")
def revenue_trend(db: Session = Depends(get_db)) -> dict:
    service = AnalyticsService(AnalyticsRepository(db))
    return success_response({"items": [i.model_dump() for i in service.revenue_trend()]})


@router.get("/order-trend")
def order_trend(db: Session = Depends(get_db)) -> dict:
    service = AnalyticsService(AnalyticsRepository(db))
    return success_response({"items": [i.model_dump() for i in service.order_trend()]})


@router.get("/top-creators")
def top_creators(limit: int = Query(default=5, ge=1, le=100), db: Session = Depends(get_db)) -> dict:
    service = AnalyticsService(AnalyticsRepository(db))
    return success_response({"items": [i.model_dump() for i in service.top_creators(limit)]})


@router.get("/top-products")
def top_products(limit: int = Query(default=5, ge=1, le=100), db: Session = Depends(get_db)) -> dict:
    service = AnalyticsService(AnalyticsRepository(db))
    return success_response({"items": [i.model_dump() for i in service.top_products(limit)]})
