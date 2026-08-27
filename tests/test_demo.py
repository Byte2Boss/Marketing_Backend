import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_available_slots(client: AsyncClient):
    response = await client.get("/api/v1/demo/available-slots?date=2026-09-15")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["date"] == "2026-09-15"
    assert len(data["data"]["available_slots"]) > 0


@pytest.mark.asyncio
async def test_book_demo_success(client: AsyncClient):
    payload = {
        "restaurant_name": "Skyline Rooftop Lounge",
        "owner_name": "Elena Rostova",
        "email": "elena@skylinelounge.com",
        "phone": "+1 555-9080",
        "tables_count": 35,
        "city": "Miami, FL",
        "preferred_date": "2026-09-15",
        "time_slot": "02:30 PM",
        "restaurant_type": "Bar / Lounge",
        "notes": "Interested in QR ordering for patio tables.",
    }
    response = await client.post("/api/v1/demo/book", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["restaurant_name"] == "Skyline Rooftop Lounge"
    assert data["data"]["time_slot"] == "02:30 PM"
    assert data["data"]["confirmation_code"].startswith("RM-")
