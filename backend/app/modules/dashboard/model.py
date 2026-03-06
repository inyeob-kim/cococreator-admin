from dataclasses import dataclass


@dataclass
class DashboardSummaryModel:
    total_creators: int
    active_brands: int
    launched_products: int
    total_revenue: float
