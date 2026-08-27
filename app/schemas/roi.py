from typing import Optional
from pydantic import BaseModel, Field

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class RoiCalculateRequest(BaseModel):
    tables_count: int = Field(..., ge=1, le=1000, description="Total number of dine-in tables")
    avg_daily_orders_per_table: int = Field(..., ge=1, le=50, description="Average turnover / orders per table per day")
    avg_order_value: float = Field(..., ge=1.0, le=10000.0, description="Average check size in USD/Currency")
    email: Optional[str] = Field(None, pattern=EMAIL_REGEX, description="Optional email to save ROI report")
    restaurant_name: Optional[str] = Field(None, max_length=150)


class RoiCalculateResponse(BaseModel):
    tables_count: int
    avg_daily_orders_per_table: int
    avg_order_value: float
    monthly_orders: int
    projected_monthly_gain: float
    projected_annual_gain: float
    projected_hours_saved_monthly: float
    turnaround_boost_percentage: float = 28.5
    ai_upsell_boost_percentage: float = 18.0
    calculation_id: Optional[str] = None
