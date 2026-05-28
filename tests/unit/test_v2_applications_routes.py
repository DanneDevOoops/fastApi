#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest
from datetime import datetime, timezone

from src.api.v2_routes import application_routes as v2_application_routes
from tests.conftest import _serialize_object, build_fake_document_class

pytestmark = pytest.mark.unit


def test_v2_application_routes(client, monkeypatch):
    monkeypatch.setattr(v2_application_routes, "model_serialize", _serialize_object)
    fake_app_cls = build_fake_document_class(
        "id",
        "index",
        "name",
        "description",
        "api_key",
        "ip_adress",
        "port",
        "tags",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    monkeypatch.setattr(v2_application_routes, "Application", fake_app_cls)

    active_app = fake_app_cls(id="app-v2-1", index=1, name="app-v2-1")
    deleted_app = fake_app_cls(
        id="app-v2-2",
        index=2,
        name="app-v2-2",
        deleted_at=datetime.now(timezone.utc),
    )
    fake_app_cls._find_result = [active_app]

    response = client.get("/api/v2/applications")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [active_app.id]

    fake_app_cls._find_one_result = active_app
    response = client.get(f"/api/v2/applications/{active_app.id}")
    assert response.status_code == 200
    assert response.json()["id"] == active_app.id

    fake_app_cls._find_result = fake_app_cls(id="app-v2-last", index=7, name="app-v2-last")
    fake_app_cls._create_result = fake_app_cls(id="app-v2-created", index=8, name="app-v2-created")
    monkeypatch.setattr(
        v2_application_routes,
        "create_application_access_token",
        lambda name, app_id: "jwt-token",
    )
    monkeypatch.setattr(v2_application_routes, "hash_key_v2", lambda token: "hashed-token")

    response = client.post(
        "/api/v2/applications",
        json={
            "id": "app-v2-created",
            "name": "app-v2-created",
            "description": "created",
            "ip_adress": "http://localhost:9001",
            "port": 9001,
            "tags": {},
        },
    )
    assert response.status_code == 201
    assert response.json()["jwt_token"] == "jwt-token"

    fake_app_cls._find_one_result = active_app
    response = client.patch(f"/api/v2/applications/delete/{active_app.id}")
    assert response.status_code == 200
    assert "soft deleted successfully" in response.json()["detail"]

    response = client.patch(
        f"/api/v2/applications/{active_app.id}",
        json={
            "name": "app-v2-updated",
            "description": "updated",
            "url": "http://localhost:9002",
            "is_active": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "app-v2-updated"

    response = client.put(
        f"/api/v2/applications/{active_app.id}",
        json={
            "name": "app-v2-replaced",
            "description": "replaced",
            "ip_adress": "http://localhost:9003",
            "port": 9010,
            "tags": {},
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "app-v2-replaced"

    response = client.delete(f"/api/v2/applications/delete/{deleted_app.id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["detail"]
