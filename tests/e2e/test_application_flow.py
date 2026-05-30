import pytest

pytestmark = pytest.mark.e2e

_BASE = "/api/v1/applications"

_APP_DEFAULTS = {
    "description": "created in e2e test",
    "url": "http://localhost:9000",
    "is_active": True,
}


def _app_payload(app_id: str, name: str = None, **overrides) -> dict:
    return {"id": app_id, "name": name or app_id, **_APP_DEFAULTS, **overrides}


@pytest.mark.asyncio
async def test_create_application_then_delete(e2e_client):
    # 1. Create application
    response = await e2e_client.post(
        "/api/v1/applications",
        json={
            "id": "e2e-app-1",
            "name": "E2E Test App",
            "description": "created in e2e test",
            "url": "http://localhost:9000",
            "is_active": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "e2e-app-1"
    assert "jwt_token" in data  # only returned at creation

    # 2. Fetch it back
    response = await e2e_client.get("/api/v1/applications/e2e-app-1")
    assert response.status_code == 200

    # 3. Soft delete it
    response = await e2e_client.patch("/api/v1/applications/delete/e2e-app-1")
    assert response.status_code == 200

    # 4. Confirm it's gone from active
    response = await e2e_client.get("/api/v1/applications/e2e-app-1")
    assert response.status_code == 404

    # 5. Confirm it appears in deleted list
    response = await e2e_client.get("/api/v1/applications/deleted")
    assert response.status_code == 200
    ids = [a["id"] for a in response.json()]
    assert "e2e-app-1" in ids

    # 6. Hard delete
    response = await e2e_client.delete("/api/v1/applications/delete/e2e-app-1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_duplicate_application_returns_409(e2e_client):
    app_id = "e2e-app-dup"
    payload = _app_payload(app_id)

    response = await e2e_client.post(_BASE, json=payload)
    assert response.status_code == 201

    # Second create with same id/name must conflict
    response = await e2e_client.post(_BASE, json=payload)
    assert response.status_code == 409

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{app_id}")


@pytest.mark.asyncio
async def test_update_application_patch(e2e_client):
    app_id = "e2e-app-patch"
    response = await e2e_client.post(_BASE, json=_app_payload(app_id))
    assert response.status_code == 201
    original = response.json()

    # PATCH only the description
    response = await e2e_client.patch(
        f"{_BASE}/{app_id}",
        json={"description": "patched description"},
    )
    assert response.status_code == 200
    updated = response.json()

    assert updated["description"] == "patched description"
    # All other fields must be unchanged
    assert updated["name"] == original["name"]
    assert updated["url"] == original["url"]
    assert updated["is_active"] == original["is_active"]

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{app_id}")


@pytest.mark.asyncio
async def test_update_application_put(e2e_client):
    app_id = "e2e-app-put"
    response = await e2e_client.post(_BASE, json=_app_payload(app_id))
    assert response.status_code == 201

    # PUT replaces all fields
    put_payload = {
        "name": "e2e-app-put",
        "description": "fully replaced description",
        "url": "http://replaced.example.com",
        "is_active": False,
    }
    response = await e2e_client.put(f"{_BASE}/{app_id}", json=put_payload)
    assert response.status_code == 200
    updated = response.json()

    assert updated["description"] == "fully replaced description"
    assert updated["url"] == "http://replaced.example.com"
    assert updated["is_active"] is False

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{app_id}")


@pytest.mark.asyncio
async def test_get_nonexistent_application_returns_404(e2e_client):
    response = await e2e_client.get(f"{_BASE}/this-id-does-not-exist")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_jwt_token_only_returned_on_creation(e2e_client):
    app_id = "e2e-app-jwt"
    response = await e2e_client.post(_BASE, json=_app_payload(app_id))
    assert response.status_code == 201
    assert "jwt_token" in response.json()

    # Subsequent GET must NOT expose the token
    response = await e2e_client.get(f"{_BASE}/{app_id}")
    assert response.status_code == 200
    assert "jwt_token" not in response.json()

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{app_id}")


# ---------------------------------------------------------------------------
# Empty state → 404
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_all_applications_empty_returns_404(e2e_client):
    response = await e2e_client.get(_BASE)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_deleted_applications_empty_returns_404(e2e_client):
    response = await e2e_client.get(f"{_BASE}/deleted")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Nonexistent resource → 404 on mutations
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_patch_nonexistent_application_returns_404(e2e_client):
    response = await e2e_client.patch(
        f"{_BASE}/no-such-app", json={"description": "x"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_put_nonexistent_application_returns_404(e2e_client):
    response = await e2e_client.put(
        f"{_BASE}/no-such-app",
        json={"name": "x", "description": "x", "url": "http://x.test", "is_active": True},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_hard_delete_nonexistent_application_returns_404(e2e_client):
    response = await e2e_client.delete(f"{_BASE}/delete/no-such-app")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# updated_at actually changes after PATCH and PUT
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_updated_at_changes_after_patch(e2e_client):
    import asyncio

    app_id = "e2e-app-updat-patch"
    response = await e2e_client.post(_BASE, json=_app_payload(app_id))
    assert response.status_code == 201
    original_updated_at = response.json()["updated_at"]

    await asyncio.sleep(0.05)

    response = await e2e_client.patch(
        f"{_BASE}/{app_id}", json={"description": "timestamp test"}
    )
    assert response.status_code == 200
    assert response.json()["updated_at"] != original_updated_at

    await e2e_client.delete(f"{_BASE}/delete/{app_id}")


@pytest.mark.asyncio
async def test_updated_at_changes_after_put(e2e_client):
    import asyncio

    app_id = "e2e-app-updat-put"
    response = await e2e_client.post(_BASE, json=_app_payload(app_id))
    assert response.status_code == 201
    original_updated_at = response.json()["updated_at"]

    await asyncio.sleep(0.05)

    response = await e2e_client.put(
        f"{_BASE}/{app_id}",
        json={"name": app_id, "description": "replaced", "url": "http://new.test", "is_active": False},
    )
    assert response.status_code == 200
    assert response.json()["updated_at"] != original_updated_at

    await e2e_client.delete(f"{_BASE}/delete/{app_id}")
