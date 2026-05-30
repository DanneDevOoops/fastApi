"""
E2E smoke tests for the utility/health-check routes.

These endpoints don't touch the database so they use a lightweight client
fixture that only overrides the health-check API key dependency — no
PostgreSQL container required.
"""

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.core.auth import get_health_check_api_key
from src.main import app

pytestmark = pytest.mark.e2e

_HEALTH_KEY = "e2e-health-test-key"
_BASE = "/api/utils"


@pytest_asyncio.fixture
async def health_client():
    """Minimal async client with health-check API key bypassed."""
    _original = app.dependency_overrides.get(get_health_check_api_key)
    app.dependency_overrides[get_health_check_api_key] = lambda: _HEALTH_KEY

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    if _original is not None:
        app.dependency_overrides[get_health_check_api_key] = _original
    else:
        app.dependency_overrides.pop(get_health_check_api_key, None)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_health_check_returns_200(health_client):
    response = await health_client.get(f"{_BASE}/health_check")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Info endpoint — verify expected fields are present
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_info_returns_expected_fields(health_client):
    response = await health_client.get(f"{_BASE}/info")
    assert response.status_code == 200
    data = response.json()
    for field in ("name", "python-version", "description", "environment"):
        assert field in data, f"Missing field '{field}' in /info response"


@pytest.mark.asyncio
async def test_pgsql_db_info_returns_expected_fields(health_client):
    response = await health_client.get(f"{_BASE}/pgsql_db_info")
    assert response.status_code == 200
    data = response.json()
    for field in ("name", "python-version", "description", "environment"):
        assert field in data, f"Missing field '{field}' in /pgsql_db_info response"


@pytest.mark.asyncio
async def test_mongo_db_info_returns_expected_fields(health_client):
    response = await health_client.get(f"{_BASE}/mongo_db_info")
    assert response.status_code == 200
    data = response.json()
    for field in ("name", "description", "environment"):
        assert field in data, f"Missing field '{field}' in /mongo_db_info response"
