#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest
from datetime import datetime, timezone
from types import SimpleNamespace

from src.api.v2_routes import user_routes as v2_user_routes
from tests.conftest import _serialize_object, build_fake_document_class

pytestmark = pytest.mark.unit


def test_v2_user_routes(client, monkeypatch):
    monkeypatch.setattr(v2_user_routes, "model_serialize", _serialize_object)
    fake_user_cls = build_fake_document_class(
        "id",
        "index",
        "username",
        "password",
        "role",
        "firstname",
        "lastname",
        "address",
        "zip_code",
        "city",
        "country",
        "phone",
        "email",
        "tags",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    monkeypatch.setattr(v2_user_routes, "User", fake_user_cls)

    active_user = fake_user_cls(id="user-v2-1", index=1, username="user-v2-1")
    deleted_user = fake_user_cls(
        id="user-v2-2",
        index=2,
        username="user-v2-2",
        deleted_at=datetime.now(timezone.utc),
    )
    fake_user_cls._find_result = [active_user]

    response = client.get("/api/v2/users")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [active_user.id]

    fake_user_cls._find_result = [deleted_user]
    response = client.get("/api/v2/users/deleted")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [deleted_user.id]

    fake_user_cls._find_one_result = active_user
    response = client.get(f"/api/v2/users/{active_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == active_user.id

    fake_user_cls._find_result = SimpleNamespace(index=9)
    fake_user_cls._create_result = fake_user_cls(id="user-v2-created", index=10, username="user-v2-created")
    monkeypatch.setattr(v2_user_routes, "hash_key_v2", lambda password: "hashed-password")

    response = client.post(
        "/api/v2/users",
        json={
            "id": "user-v2-created",
            "username": "user-v2-created",
            "email": "user-v2-created@example.com",
            "password": "password",
            "firstname": "First",
            "lastname": "Last",
            "address": "Main Street 1",
            "zip_code": "12345",
            "city": "City",
            "country": "Country",
            "phone": "1234567890",
            "tags": {},
        },
    )
    assert response.status_code == 201
    assert response.json()["id"] == "user-v2-created"
    assert "password" not in response.json()

    fake_user_cls._find_result = [active_user]
    response = client.post("/api/v2/users/batch", json={"id": [active_user.id, deleted_user.id]})
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [active_user.id]

    fake_user_cls._find_one_result = active_user
    response = client.patch(f"/api/v2/users/delete/{active_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == active_user.id
    assert response.json()["deleted_at"] is not None

    response = client.patch(
        f"/api/v2/users/{active_user.id}",
        json={"firstname": "Updated", "is_active": False},
    )
    assert response.status_code == 200
    assert response.json()["firstname"] == "Updated"

    response = client.put(
        f"/api/v2/users/{active_user.id}",
        json={
            "firstname": "Replaced",
            "lastname": "User",
            "address": "Other Street 1",
            "zip_code": "11111",
            "city": "Other City",
            "country": "Other Country",
            "phone": "9999999999",
            "tags": {},
        },
    )
    assert response.status_code == 200
    assert response.json()["firstname"] == "Replaced"

    response = client.delete(f"/api/v2/users/delete/{deleted_user.id}")
    assert response.status_code == 204
