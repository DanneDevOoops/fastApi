#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import asyncio
from datetime import datetime, timezone

from tests.conftest import _insert_v1_application


def test_v1_application_options_route(client, health_headers):
    response = client.options("/api/v1/applications", headers=health_headers)
    assert response.status_code == 204
    assert response.headers["allow"] == "GET, POST, PUT, PATCH, DELETE"


def test_v1_application_routes(client):
    active_app = asyncio.run(
        _insert_v1_application(id="app-1", name="app-1", description="active")
    )
    deleted_app = asyncio.run(
        _insert_v1_application(
            id="app-2",
            name="app-2",
            description="deleted",
            deleted_at=datetime.now(timezone.utc),
        )
    )

    response = client.get("/api/v1/applications")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {active_app.id}

    response = client.get("/api/v1/applications/deleted")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {deleted_app.id}

    response = client.get(f"/api/v1/applications/{active_app.id}")
    assert response.status_code == 200
    assert response.json()["id"] == active_app.id

    response = client.post(
        "/api/v1/applications",
        json={
            "id": "app-3",
            "name": "app-3",
            "description": "created",
            "url": "http://localhost:9001",
            "is_active": True,
        },
    )
    assert response.status_code == 201
    assert response.json()["id"] == "app-3"
    assert response.json()["jwt_token"]

    response = client.patch(
        f"/api/v1/applications/{active_app.id}",
        json={
            "name": "app-1-updated",
            "description": "updated",
            "url": "http://localhost:9010",
            "is_active": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "app-1-updated"

    response = client.put(
        f"/api/v1/applications/{active_app.id}",
        json={
            "name": "app-1-replaced",
            "description": "replaced",
            "url": "http://localhost:9020",
            "is_active": True,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "app-1-replaced"

    response = client.patch(f"/api/v1/applications/delete/{active_app.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == f"Application {active_app.id} soft deleted successfully"

    response = client.delete(f"/api/v1/applications/delete/{deleted_app.id}")
    assert response.status_code == 200
