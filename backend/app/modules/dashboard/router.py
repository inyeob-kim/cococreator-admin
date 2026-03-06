from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.api.response import success_response
from app.core.database import get_db
from app.modules.dashboard.constants import DASHBOARD_TAG
from app.modules.dashboard.repository import DashboardRepository
from app.modules.dashboard.service import DashboardService

router = APIRouter(prefix="/dashboard", tags=[DASHBOARD_TAG])


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)) -> dict:
    service = DashboardService(DashboardRepository(db))
    return success_response(service.get_summary().model_dump())


@router.get("/creator-pipeline")
def get_dashboard_creator_pipeline(db: Session = Depends(get_db)) -> dict:
    service = DashboardService(DashboardRepository(db))
    return success_response({"items": [i.model_dump() for i in service.get_creator_pipeline()]})


@router.get("/top-products")
def get_dashboard_top_products(limit: int = Query(default=5, ge=1, le=50), db: Session = Depends(get_db)) -> dict:
    service = DashboardService(DashboardRepository(db))
    return success_response({"items": [i.model_dump() for i in service.get_top_products(limit)]})
