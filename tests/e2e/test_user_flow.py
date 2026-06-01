import os

import pytest

pytestmark = pytest.mark.e2e

_BASE = "/api/v1/users"

_USER_DEFAULTS = {
    "password": os.environ.get("E2E_TEST_PASSWORD", "test-password-e2e"),
    "first_name": "E2E",
    "last_name": "Test",
    "phone_number": "+1234567890",
    "address": "123 Test St",
    "city": "Testville",
    "state": "TS",
    "country": "Testland",
    "zip_code": "00000",
    "is_active": True,
    "is_superuser": False,
}


def _user_payload(
    user_id: str, username: str = None, email: str = None, **overrides
) -> dict:
    return {
        "id": user_id,
        "username": username or user_id,
        "email": email or f"{user_id}@e2e.test",
        **_USER_DEFAULTS,
        **overrides,
    }


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_user_full_lifecycle(e2e_client):
    user_id = "e2e-user-lifecycle"

    # 1. Create
    response = await e2e_client.post(_BASE, json=_user_payload(user_id))
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == user_id

    # 2. Fetch by ID
    response = await e2e_client.get(f"{_BASE}/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

    # 3. Appears in active list
    response = await e2e_client.get(_BASE)
    assert response.status_code == 200
    ids = [u["id"] for u in response.json()]
    assert user_id in ids

    # 4. Soft delete
    response = await e2e_client.patch(f"{_BASE}/delete/{user_id}")
    assert response.status_code == 200

    # 5. No longer in active list
    response = await e2e_client.get(f"{_BASE}/{user_id}")
    assert response.status_code == 404

    # 6. Appears in soft-deleted list
    response = await e2e_client.get(f"{_BASE}/deleted")
    assert response.status_code == 200
    ids = [u["id"] for u in response.json()]
    assert user_id in ids

    # 7. Hard delete (user routes return 204 No Content)
    response = await e2e_client.delete(f"{_BASE}/delete/{user_id}")
    assert response.status_code == 204


# ---------------------------------------------------------------------------
# Duplicate user → 409
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_duplicate_user_returns_409(e2e_client):
    user_id = "e2e-user-dup"
    payload = _user_payload(user_id)

    response = await e2e_client.post(_BASE, json=payload)
    assert response.status_code == 201

    response = await e2e_client.post(_BASE, json=payload)
    assert response.status_code == 409

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{user_id}")


# ---------------------------------------------------------------------------
# Password must NOT appear in any response
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_password_not_in_response(e2e_client):
    user_id = "e2e-user-pwd"

    # Not in create response
    response = await e2e_client.post(_BASE, json=_user_payload(user_id))
    assert response.status_code == 201
    assert "password" not in response.json()

    # Not in GET by ID response
    response = await e2e_client.get(f"{_BASE}/{user_id}")
    assert response.status_code == 200
    assert "password" not in response.json()

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{user_id}")


# ---------------------------------------------------------------------------
# PATCH partial update
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_patch_update_user(e2e_client):
    user_id = "e2e-user-patch"
    response = await e2e_client.post(_BASE, json=_user_payload(user_id))
    assert response.status_code == 201
    original = response.json()

    response = await e2e_client.patch(
        f"{_BASE}/{user_id}", json={"city": "Patchedtown"}
    )
    assert response.status_code == 200
    updated = response.json()

    assert updated["city"] == "Patchedtown"
    # Unchanged fields must remain the same
    assert updated["username"] == original["username"]
    assert updated["email"] == original["email"]
    assert updated["first_name"] == original["first_name"]

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{user_id}")


# ---------------------------------------------------------------------------
# PUT full replace
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_put_update_user(e2e_client):
    user_id = "e2e-user-put"
    response = await e2e_client.post(_BASE, json=_user_payload(user_id))
    assert response.status_code == 201

    put_payload = {
        **_USER_DEFAULTS,
        "username": user_id,
        "email": f"{user_id}@replaced.test",
        "city": "Replacedville",
        "country": "Newland",
    }
    response = await e2e_client.put(f"{_BASE}/{user_id}", json=put_payload)
    assert response.status_code == 200
    updated = response.json()

    assert updated["city"] == "Replacedville"
    assert updated["country"] == "Newland"
    assert updated["email"] == f"{user_id}@replaced.test"

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{user_id}")


# ---------------------------------------------------------------------------
# /activated — only active users
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_activated_users(e2e_client):
    active_id = "e2e-user-active"
    inactive_id = "e2e-user-inactive"

    await e2e_client.post(_BASE, json=_user_payload(active_id, is_active=True))
    await e2e_client.post(_BASE, json=_user_payload(inactive_id, is_active=False))

    response = await e2e_client.get(f"{_BASE}/activated")
    assert response.status_code == 200
    ids = [u["id"] for u in response.json()]
    assert active_id in ids
    assert inactive_id not in ids

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{active_id}")
    await e2e_client.delete(f"{_BASE}/delete/{inactive_id}")


# ---------------------------------------------------------------------------
# /deactivated — only inactive users
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_deactivated_users(e2e_client):
    active_id = "e2e-user-act2"
    inactive_id = "e2e-user-inact2"

    await e2e_client.post(_BASE, json=_user_payload(active_id, is_active=True))
    await e2e_client.post(_BASE, json=_user_payload(inactive_id, is_active=False))

    response = await e2e_client.get(f"{_BASE}/deactivated")
    assert response.status_code == 200
    ids = [u["id"] for u in response.json()]
    assert inactive_id in ids
    assert active_id not in ids

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{active_id}")
    await e2e_client.delete(f"{_BASE}/delete/{inactive_id}")


# ---------------------------------------------------------------------------
# /superusers — only superusers
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_superusers(e2e_client):
    regular_id = "e2e-user-regular"
    super_id = "e2e-user-super"

    await e2e_client.post(_BASE, json=_user_payload(regular_id, is_superuser=False))
    await e2e_client.post(_BASE, json=_user_payload(super_id, is_superuser=True))

    response = await e2e_client.get(f"{_BASE}/superusers")
    assert response.status_code == 200
    ids = [u["id"] for u in response.json()]
    assert super_id in ids
    assert regular_id not in ids

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{regular_id}")
    await e2e_client.delete(f"{_BASE}/delete/{super_id}")


# ---------------------------------------------------------------------------
# POST /users/batch — returns exactly the requested IDs
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_batch_get_users_by_ids(e2e_client):
    ids = [f"e2e-batch-user-{i}" for i in range(3)]
    for uid in ids:
        await e2e_client.post(_BASE, json=_user_payload(uid))

    # Request only the first two
    response = await e2e_client.post(f"{_BASE}/batch", json={"id": ids[:2]})
    assert response.status_code == 200
    returned_ids = {u["id"] for u in response.json()}
    assert returned_ids == set(ids[:2])
    assert ids[2] not in returned_ids

    # Cleanup
    for uid in ids:
        await e2e_client.delete(f"{_BASE}/delete/{uid}")


# ---------------------------------------------------------------------------
# GET /users on nonexistent user → 404
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_nonexistent_user_returns_404(e2e_client):
    response = await e2e_client.get(f"{_BASE}/this-id-does-not-exist")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Password never exposed in ANY response (list, update, batch)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_password_not_in_list_responses(e2e_client):
    uid_active = "e2e-pwd-list-active"
    uid_inactive = "e2e-pwd-list-inactive"
    uid_super = "e2e-pwd-list-super"

    await e2e_client.post(_BASE, json=_user_payload(uid_active, is_active=True))
    await e2e_client.post(_BASE, json=_user_payload(uid_inactive, is_active=False))
    await e2e_client.post(_BASE, json=_user_payload(uid_super, is_superuser=True))

    for endpoint in ("/activated", "/deactivated", "/superusers", ""):
        response = await e2e_client.get(f"{_BASE}{endpoint}")
        assert response.status_code == 200, f"Unexpected status on {endpoint}"
        for user in response.json():
            assert "password" not in user, f"password exposed in GET {endpoint}"

    # Soft-delete one then check /deleted
    await e2e_client.patch(f"{_BASE}/delete/{uid_active}")
    response = await e2e_client.get(f"{_BASE}/deleted")
    assert response.status_code == 200
    for user in response.json():
        assert "password" not in user, "password exposed in GET /deleted"

    # Batch response
    response = await e2e_client.post(
        f"{_BASE}/batch", json={"id": [uid_inactive, uid_super]}
    )
    assert response.status_code == 200
    for user in response.json():
        assert "password" not in user, "password exposed in POST /batch"

    # PATCH response
    response = await e2e_client.patch(
        f"{_BASE}/{uid_inactive}", json={"city": "PatchCity"}
    )
    assert response.status_code == 200
    assert "password" not in response.json(), "password exposed in PATCH response"

    # PUT response
    response = await e2e_client.put(f"{_BASE}/{uid_super}", json={"city": "PutCity"})
    assert response.status_code == 200
    assert "password" not in response.json(), "password exposed in PUT response"

    # Cleanup
    for uid in (uid_active, uid_inactive, uid_super):
        await e2e_client.delete(f"{_BASE}/delete/{uid}")


# ---------------------------------------------------------------------------
# Empty list endpoints → 404
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_all_users_empty_returns_404(e2e_client):
    response = await e2e_client.get(_BASE)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_deleted_users_empty_returns_404(e2e_client):
    response = await e2e_client.get(f"{_BASE}/deleted")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_activated_users_empty_returns_404(e2e_client):
    response = await e2e_client.get(f"{_BASE}/activated")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_deactivated_users_empty_returns_404(e2e_client):
    response = await e2e_client.get(f"{_BASE}/deactivated")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_superusers_empty_returns_404(e2e_client):
    response = await e2e_client.get(f"{_BASE}/superusers")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Nonexistent resource → 404 on mutations
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_patch_nonexistent_user_returns_404(e2e_client):
    response = await e2e_client.patch(f"{_BASE}/no-such-user", json={"city": "x"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_put_nonexistent_user_returns_404(e2e_client):
    response = await e2e_client.put(f"{_BASE}/no-such-user", json={"city": "x"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_soft_delete_nonexistent_user_returns_404(e2e_client):
    response = await e2e_client.patch(f"{_BASE}/delete/no-such-user")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_hard_delete_nonexistent_user_returns_404(e2e_client):
    response = await e2e_client.delete(f"{_BASE}/delete/no-such-user")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Response field consistency — password never exposed, is_superuser absent on create
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_response_excludes_sensitive_fields(e2e_client):
    user_id = "e2e-user-fields"
    response = await e2e_client.post(
        _BASE, json=_user_payload(user_id, is_superuser=True)
    )
    assert response.status_code == 201
    data = response.json()

    # Sensitive fields must be absent from the create response
    assert "password" not in data
    assert "is_superuser" not in data
    assert "updated_at" not in data
    assert "deleted_at" not in data

    # GET responses must also never expose the password
    response = await e2e_client.get(f"{_BASE}/{user_id}")
    assert response.status_code == 200
    assert "password" not in response.json()

    response = await e2e_client.get(_BASE)
    assert response.status_code == 200
    for user in response.json():
        assert "password" not in user

    # Cleanup
    await e2e_client.delete(f"{_BASE}/delete/{user_id}")


# ---------------------------------------------------------------------------
# updated_at actually changes after PATCH and PUT
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_updated_at_changes_after_patch(e2e_client):
    import asyncio

    user_id = "e2e-user-updat-patch"
    response = await e2e_client.post(_BASE, json=_user_payload(user_id))
    assert response.status_code == 201

    # Fetch to capture the initial updated_at
    response = await e2e_client.get(f"{_BASE}/{user_id}")
    original_updated_at = response.json()["updated_at"]

    await asyncio.sleep(0.05)  # ensure clock advances

    response = await e2e_client.patch(
        f"{_BASE}/{user_id}", json={"city": "TimestampTown"}
    )
    assert response.status_code == 200
    assert response.json()["updated_at"] != original_updated_at

    await e2e_client.delete(f"{_BASE}/delete/{user_id}")


@pytest.mark.asyncio
async def test_updated_at_changes_after_put(e2e_client):
    import asyncio

    user_id = "e2e-user-updat-put"
    response = await e2e_client.post(_BASE, json=_user_payload(user_id))
    assert response.status_code == 201

    response = await e2e_client.get(f"{_BASE}/{user_id}")
    original_updated_at = response.json()["updated_at"]

    await asyncio.sleep(0.05)

    response = await e2e_client.put(f"{_BASE}/{user_id}", json={"country": "Newland"})
    assert response.status_code == 200
    assert response.json()["updated_at"] != original_updated_at

    await e2e_client.delete(f"{_BASE}/delete/{user_id}")


# ---------------------------------------------------------------------------
# Batch with unknown IDs → partial match (only known IDs returned)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_batch_partial_match_returns_only_known_ids(e2e_client):
    uid_a = "e2e-batch-partial-a"
    uid_b = "e2e-batch-partial-b"

    await e2e_client.post(_BASE, json=_user_payload(uid_a))
    await e2e_client.post(_BASE, json=_user_payload(uid_b))

    response = await e2e_client.post(
        f"{_BASE}/batch",
        json={"id": [uid_a, "does-not-exist-1", uid_b, "does-not-exist-2"]},
    )
    assert response.status_code == 200
    returned_ids = {u["id"] for u in response.json()}
    assert returned_ids == {uid_a, uid_b}

    await e2e_client.delete(f"{_BASE}/delete/{uid_a}")
    await e2e_client.delete(f"{_BASE}/delete/{uid_b}")
