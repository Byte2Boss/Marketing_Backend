from sqlalchemy.ext.asyncio import AsyncSession
from app.models.roi import RoiCalculation
from app.schemas.roi import RoiCalculateRequest, RoiCalculateResponse
from app.core.security import normalize_email


async def calculate_and_save_roi(db: AsyncSession, request: RoiCalculateRequest) -> RoiCalculateResponse:
    """
    Calculate dynamic ROI based on hospitality empirical benchmarks:
    - Monthly Orders = tables_count * avg_daily_orders_per_table * 30 days
    - Gross Monthly GMV = monthly_orders * avg_order_value
    - AI Upsell Lift = 18.0% (smart beverage & side pairing suggestions)
    - Projected Monthly Gain = GMV * 0.18
    - Projected Annual Gain = Projected Monthly Gain * 12
    - Projected Hours Saved = tables_count * 1.5 hours/table/month in staff turnover efficiency
    """
    monthly_orders = request.tables_count * request.avg_daily_orders_per_table * 30
    gross_monthly_gmv = monthly_orders * request.avg_order_value
    
    ai_upsell_boost_pct = 18.0
    projected_monthly_gain = round(gross_monthly_gmv * (ai_upsell_boost_pct / 100.0), 2)
    projected_annual_gain = round(projected_monthly_gain * 12.0, 2)
    
    # 1.5 labor hours saved per table each month through automated contactless QR ordering
    projected_hours_saved = round(request.tables_count * 1.5 * 30 / 10, 1)

    calc_id = None
    if request.email:
        clean_email = normalize_email(request.email)
        record = RoiCalculation(
            email=clean_email,
            restaurant_name=request.restaurant_name,
            tables_count=request.tables_count,
            avg_daily_orders=request.avg_daily_orders_per_table,
            avg_order_value=request.avg_order_value,
            projected_monthly_gain=projected_monthly_gain,
            projected_hours_saved=projected_hours_saved,
        )
        db.add(record)
        await db.commit()
        await db.refresh(record)
        calc_id = record.id

    return RoiCalculateResponse(
        tables_count=request.tables_count,
        avg_daily_orders_per_table=request.avg_daily_orders_per_table,
        avg_order_value=request.avg_order_value,
        monthly_orders=monthly_orders,
        projected_monthly_gain=projected_monthly_gain,
        projected_annual_gain=projected_annual_gain,
        projected_hours_saved_monthly=projected_hours_saved,
        turnaround_boost_percentage=28.5,
        ai_upsell_boost_percentage=ai_upsell_boost_pct,
        calculation_id=calc_id,
    )
