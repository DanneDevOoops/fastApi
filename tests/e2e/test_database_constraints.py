"""
E2E tests that verify real PostgreSQL constraints — things SQLite either
ignores or handles differently (unique indexes, referential integrity, etc.).
"""

import os

import pytest

pytestmark = pytest.mark.e2e

_APPS = "/api/v1/applications"
_USERS = "/api/v1/users"

_APP_DEFAULTS = {
    "description": "constraint test",
    "url": "http://localhost:9000",
    "is_active": True,
}

_USER_DEFAULTS = {
    "password": os.environ.get("E2E_TEST_PASSWORD", "test-password-e2e"),
    "first_name": "Constraint",
    "last_name": "Test",
    "phone_number": "+1234567890",
    "address": "1 Constraint Ave",
    "city": "DBCity",
    "state": "DB",
    "country": "DBLand",
    "zip_code": "00000",
    "is_active": True,
    "is_superuser": False,
}


def _app_payload(app_id: str, **overrides) -> dict:
    return {"id": app_id, "name": app_id, **_APP_DEFAULTS, **overrides}


def _user_payload(user_id: str, **overrides) -> dict:
    return {
        "id": user_id,
        "username": user_id,
        "email": f"{user_id}@constraint.test",
        **_USER_DEFAULTS,
        **overrides,
    }


# ---------------------------------------------------------------------------
# Unique constraint: application name
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_unique_constraint_application_name(e2e_client):
    """Two applications with the same name must return 409."""
    name = "constraint-unique-app-name"
    payload_a = {"id": "constraint-app-a", "name": name, **_APP_DEFAULTS}
    payload_b = {"id": "constraint-app-b", "name": name, **_APP_DEFAULTS}

    response = await e2e_client.post(_APPS, json=payload_a)
    assert response.status_code == 201

    response = await e2e_client.post(_APPS, json=payload_b)
    assert response.status_code == 409

    # Cleanup
    await e2e_client.delete(f"{_APPS}/delete/constraint-app-a")


# ---------------------------------------------------------------------------
# Unique constraint: user email
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_unique_constraint_user_email(e2e_client):
    """Two users sharing the same email must return 409."""
    shared_email = "shared@constraint.test"

    response = await e2e_client.post(
        _USERS, json=_user_payload("constraint-user-a", email=shared_email)
    )
    assert response.status_code == 201

    response = await e2e_client.post(
        _USERS, json=_user_payload("constraint-user-b", email=shared_email)
    )
    assert response.status_code == 409

    # Cleanup
    await e2e_client.delete(f"{_USERS}/delete/constraint-user-a")


# ---------------------------------------------------------------------------
# Soft-delete idempotency: second soft delete → 404
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_soft_delete_twice_returns_404(e2e_client):
    """Soft-deleting an already soft-deleted resource must return 404."""
    app_id = "constraint-app-softdel"

    response = await e2e_client.post(_APPS, json=_app_payload(app_id))
    assert response.status_code == 201

    response = await e2e_client.patch(f"{_APPS}/delete/{app_id}")
    assert response.status_code == 200

    response = await e2e_client.patch(f"{_APPS}/delete/{app_id}")
    assert response.status_code == 404

    # Cleanup
    await e2e_client.delete(f"{_APPS}/delete/{app_id}")


@pytest.mark.asyncio
async def test_user_soft_delete_twice_returns_404(e2e_client):
    """Soft-deleting an already soft-deleted user must return 404."""
    user_id = "constraint-user-softdel"

    response = await e2e_client.post(_USERS, json=_user_payload(user_id))
    assert response.status_code == 201

    response = await e2e_client.patch(f"{_USERS}/delete/{user_id}")
    assert response.status_code == 200

    response = await e2e_client.patch(f"{_USERS}/delete/{user_id}")
    assert response.status_code == 404

    # Cleanup
    await e2e_client.delete(f"{_USERS}/delete/{user_id}")


# ---------------------------------------------------------------------------
# Hard delete then GET → 404
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_hard_delete_then_get_returns_404(e2e_client):
    """After a hard delete the resource must no longer exist."""
    app_id = "constraint-app-harddel"

    response = await e2e_client.post(_APPS, json=_app_payload(app_id))
    assert response.status_code == 201

    # Soft-delete first (required before hard delete on most flows)
    await e2e_client.patch(f"{_APPS}/delete/{app_id}")

    response = await e2e_client.delete(f"{_APPS}/delete/{app_id}")
    assert response.status_code == 200

    # Should be gone entirely
    response = await e2e_client.get(f"{_APPS}/{app_id}")
    assert response.status_code == 404
