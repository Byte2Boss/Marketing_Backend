import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_pricing_content(client: AsyncClient):
    """Test fetching pricing tiers and comparison matrix."""
    response = await client.get("/api/v1/content/pricing")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "tiers" in data["data"]
    assert "matrix" in data["data"]
    assert len(data["data"]["tiers"]) >= 1


@pytest.mark.asyncio
async def test_get_testimonials_content(client: AsyncClient):
    """Test fetching testimonials and trust stats."""
    response = await client.get("/api/v1/content/testimonials")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "testimonials" in data["data"]
    assert "trust_stats" in data["data"]


@pytest.mark.asyncio
async def test_get_faqs_content(client: AsyncClient):
    """Test fetching categorized FAQs."""
    response = await client.get("/api/v1/content/faqs")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "categories" in data["data"]
    assert "faqs" in data["data"]


@pytest.mark.asyncio
async def test_get_features_content(client: AsyncClient):
    """Test fetching feature deep dives."""
    response = await client.get("/api/v1/content/features")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1


@pytest.mark.asyncio
async def test_get_concepts_content(client: AsyncClient):
    """Test fetching interactive simulator concepts and dishes."""
    response = await client.get("/api/v1/content/concepts")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1
