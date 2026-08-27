import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_contact_inquiry_success(client: AsyncClient):
    payload = {
        "full_name": "Alexander Hayes",
        "email": "alex@chainsgroup.com",
        "phone": "+1 555-7788",
        "subject": "Franchise inquiry for 8 locations",
        "message": "We would like to request enterprise multi-unit pricing and custom integrations.",
    }
    response = await client.post("/api/v1/contact", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["full_name"] == "Alexander Hayes"
    assert data["data"]["subject"] == "Franchise inquiry for 8 locations"


@pytest.mark.asyncio
async def test_newsletter_subscribe_success(client: AsyncClient):
    payload = {
        "email": "newsletter.reader@culinary.com",
        "source": "footer_signup",
    }
    response = await client.post("/api/v1/newsletter/subscribe", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "newsletter.reader@culinary.com"
    assert data["data"]["is_active"] is True
