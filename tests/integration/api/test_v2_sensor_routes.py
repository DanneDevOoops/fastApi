#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

from datetime import datetime, timezone

import pytest

from src.api.v2_routes import sensor_routes as v2_sensor_routes
from tests.conftest import _serialize_object, build_fake_document_class

pytestmark = pytest.mark.integration


def test_v2_sensor_routes(client, monkeypatch):
    monkeypatch.setattr(v2_sensor_routes, "model_serialize", _serialize_object)
    fake_sensor_cls = build_fake_document_class(
        "id",
        "index",
        "name",
        "value_unit",
        "location",
        "device_id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    monkeypatch.setattr(v2_sensor_routes, "Sensor", fake_sensor_cls)

    active_sensor = fake_sensor_cls(id="sensor-v2-1", index=1, name="sensor-v2-1")
    deleted_sensor = fake_sensor_cls(
        id="sensor-v2-2",
        index=2,
        name="sensor-v2-2",
        deleted_at=datetime.now(timezone.utc),
    )
    fake_sensor_cls._find_result = [active_sensor]

    response = client.get("/api/v2/sensors")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [active_sensor.id]

    fake_sensor_cls._find_result = [deleted_sensor]
    response = client.get("/api/v2/sensors/deleted")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [deleted_sensor.id]

    fake_sensor_cls._find_result = active_sensor
    response = client.get(f"/api/v2/sensors/{active_sensor.id}")
    assert response.status_code == 200
    assert response.json()["id"] == active_sensor.id

    fake_sensor_cls._find_result = fake_sensor_cls(
        id="sensor-v2-last", index=8, name="sensor-v2-last"
    )
    fake_sensor_cls._create_result = fake_sensor_cls(
        id="sensor-v2-created", index=9, name="sensor-v2-created"
    )
    response = client.post(
        "/api/v2/sensors",
        json={
            "name": "sensor-v2-created",
            "value_unit": "C",
            "location": "lab",
            "device_id": "device-1",
        },
    )
    assert response.status_code == 201
    assert response.json()["id"] == "sensor-v2-created"

    fake_sensor_cls._find_one_result = active_sensor
    response = client.patch(f"/api/v2/sensors/delete/{active_sensor.id}")
    assert response.status_code == 200
    assert response.json()["id"] == active_sensor.id

    fake_sensor_cls._find_result = active_sensor
    response = client.patch(
        f"/api/v2/sensors/{active_sensor.id}",
        json={"name": "sensor-v2-updated", "location": "field"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "sensor-v2-updated"

    response = client.put(
        f"/api/v2/sensors/{active_sensor.id}",
        json={
            "name": "sensor-v2-replaced",
            "value_unit": "F",
            "location": "office",
            "device_id": "device-2",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "sensor-v2-replaced"

    fake_sensor_cls._find_one_result = deleted_sensor
    response = client.delete(f"/api/v2/sensors/delete/{deleted_sensor.id}")
    assert response.status_code == 204
