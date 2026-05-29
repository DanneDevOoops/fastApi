#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest

pytestmark = pytest.mark.integration


def test_app_health_check(client, health_headers) -> None:
    response = client.get("/api/utils/health_check", headers=health_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == "Server is OK"


def test_app_health_check_no_key(client) -> None:
    response = client.get("/api/utils/health_check")
    assert response.status_code == 401


def test_app_health_check_wrong_key(client) -> None:
    response = client.get("/api/utils/health_check", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401


def test_app_info(client, health_headers) -> None:
    response = client.get("/api/utils/info", headers=health_headers)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "environment" in data
    assert "python-version" in data


def test_pgsql_db_info(client, health_headers) -> None:
    response = client.get("/api/utils/pgsql_db_info", headers=health_headers)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "environment" in data


def test_mongo_db_info(client, health_headers) -> None:
    response = client.get("/api/utils/mongo_db_info", headers=health_headers)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "environment" in data
