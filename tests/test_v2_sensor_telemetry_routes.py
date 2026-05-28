#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

from unittest.mock import AsyncMock

import pytest

from src.api.v2_routes import sensor_telemetry_routes as v2_sensor_telemetry_routes
from tests.conftest import _serialize_object, build_fake_document_class


def test_v2_sensor_telemetry_routes(client, monkeypatch):
    monkeypatch.setattr(v2_sensor_telemetry_routes, "model_serialize", _serialize_object)
    fake_telemetry_cls = build_fake_document_class("id", "time", "key", "value", "sensor_id")
    monkeypatch.setattr(v2_sensor_telemetry_routes, "SensorTelemetry", fake_telemetry_cls)

    telemetry = fake_telemetry_cls(id="telemetry-v2-1", key="temperature", value=21.5)
    fake_telemetry_cls._find_result = [telemetry]
    response = client.get("/api/v2/sensor_telemetry")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [telemetry.id]

    response = client.get("/api/v2/sensor_telemetry/sensor-v2-1")
    assert response.status_code == 200
    assert "sensor-v2-1" in response.json()

    fake_telemetry_cls._create_result = fake_telemetry_cls(id="telemetry-v2-created")
    response = client.post(
        "/api/v2/sensor_telemetry",
        json={"key": "temperature", "value": 22.0, "sensor_id": "sensor-v2-1"},
    )
    assert response.status_code == 201
    assert response.json()["id"] == "telemetry-v2-created"

    monkeypatch.setattr(v2_sensor_telemetry_routes.asyncio, "sleep", AsyncMock(return_value=None))
    fake_telemetry_cls._create_result = fake_telemetry_cls(id="telemetry-v2-batch")
    response = client.post("/api/v2/sensor_telemetry/fake_some?number_of_items=2&interval=0")
    assert response.status_code == 201
    assert len(response.json()) == 2


@pytest.mark.xfail(reason="Filtered telemetry route is currently broken")
def test_v2_sensor_telemetry_filtered_route_is_broken(client):
    response = client.post(
        "/api/v2/sensor_telemetry/filtered",
        json={"sensor_id": "sensor-v2-1", "key": "temperature", "value": 22.0},
    )
    assert response.status_code == 200


@pytest.mark.xfail(reason="Telemetry update route is currently incomplete")
def test_v2_sensor_telemetry_update_route_is_broken(client):
    response = client.patch("/api/v2/sensor_telemetry/sensor-v2-1")
    assert response.status_code == 200
