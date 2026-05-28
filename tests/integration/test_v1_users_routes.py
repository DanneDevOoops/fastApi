#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest
import asyncio
from datetime import datetime, timezone

from tests.conftest import _insert_v1_user

pytestmark = pytest.mark.integration


def test_v1_user_options_route(client, health_headers):
    response = client.options("/api/v1/users", headers=health_headers)
    assert response.status_code == 204
    assert response.headers["allow"] == "GET, POST, PUT, PATCH, DELETE"


def test_v1_user_routes(client):
    active_user = asyncio.run(
        _insert_v1_user(id="user-1", username="user-1", email="user-1@example.com")
    )
    inactive_user = asyncio.run(
        _insert_v1_user(
            id="user-2",
            username="user-2",
            email="user-2@example.com",
            is_active=False,
        )
    )
    deleted_user = asyncio.run(
        _insert_v1_user(
            id="user-3",
            username="user-3",
            email="user-3@example.com",
            deleted_at=datetime.now(timezone.utc),
        )
    )
    superuser = asyncio.run(
        _insert_v1_user(
            id="user-4",
            username="user-4",
            email="user-4@example.com",
            is_superuser=True,
        )
    )

    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {
        active_user.id,
        inactive_user.id,
        superuser.id,
    }

    response = client.get("/api/v1/users/deleted")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {deleted_user.id}

    response = client.get("/api/v1/users/activated")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {active_user.id, superuser.id}

    response = client.get("/api/v1/users/deactivated")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {inactive_user.id}

    response = client.get("/api/v1/users/superusers")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {superuser.id}

    response = client.get(f"/api/v1/users/{active_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == active_user.id

    response = client.post(
        "/api/v1/users",
        json={
            "id": "user-5",
            "username": "user-5",
            "email": "user-5@example.com",
            "password": "secret-pass",
            "first_name": "User",
            "last_name": "Five",
            "phone_number": "1234567890",
            "address": "Main Street 5",
            "city": "City",
            "state": "State",
            "country": "Country",
            "zip_code": "54321",
            "is_active": True,
            "is_superuser": False,
        },
    )
    assert response.status_code == 201
    assert response.json()["id"] == "user-5"
    assert "password" not in response.json()

    response = client.post("/api/v1/users/batch", json=[active_user.id, inactive_user.id])
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {active_user.id, inactive_user.id}

    response = client.patch(
        f"/api/v1/users/{active_user.id}",
        json={"first_name": "Updated", "is_active": False},
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"

    response = client.put(
        f"/api/v1/users/{active_user.id}",
        json={
            "username": "user-1-replaced",
            "email": "user-1-replaced@example.com",
            "password": "new-secret",
            "first_name": "Replaced",
            "last_name": "User",
            "phone_number": "9999999999",
            "address": "Other Street 1",
            "city": "Other City",
            "state": "Other State",
            "country": "Other Country",
            "zip_code": "11111",
            "is_active": True,
            "is_superuser": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "user-1-replaced"

    response = client.patch(f"/api/v1/users/delete/{active_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == active_user.id
    assert response.json()["deleted_at"] is not None

    response = client.delete(f"/api/v1/users/delete/{inactive_user.id}")
    assert response.status_code == 204
