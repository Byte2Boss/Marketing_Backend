import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_lead_success(client: AsyncClient):
    payload = {
        "restaurant_name": "Trattoria Roma",
        "owner_name": "Giovanni Rossi",
        "email": "giovanni@trattoria.com",
        "phone": "+1 555-0123",
        "tables_count": 22,
        "city": "Boston, MA",
        "source": "hero_cta",
    }
    response = await client.post("/api/v1/leads", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["restaurant_name"] == "Trattoria Roma"
    assert data["data"]["email"] == "giovanni@trattoria.com"
    assert data["data"]["status"] == "new"


@pytest.mark.asyncio
async def test_register_lead_validation_error(client: AsyncClient):
    # Missing required restaurant_name and invalid email
    payload = {
        "owner_name": "Giovanni Rossi",
        "email": "invalid-email-format",
        "tables_count": -5,
    }
    response = await client.post("/api/v1/leads", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"
