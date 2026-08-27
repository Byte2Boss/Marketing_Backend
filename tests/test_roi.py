import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_roi_calculation_success(client: AsyncClient):
    payload = {
        "tables_count": 20,
        "avg_daily_orders_per_table": 5,
        "avg_order_value": 35.0,
        "email": "test@bistro.com",
        "restaurant_name": "Bistro Verde",
    }
    response = await client.post("/api/v1/roi/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res = data["data"]
    # 20 * 5 * 30 = 3000 monthly orders
    assert res["monthly_orders"] == 3000
    # 3000 * 35 = 105,000 GMV -> 18% lift = 18,900
    assert res["projected_monthly_gain"] == 18900.0
    assert res["projected_annual_gain"] == 18900.0 * 12
    assert res["calculation_id"] is not None
