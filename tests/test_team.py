import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_team_members(client: AsyncClient):
    response = await client.get("/api/v1/team")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
