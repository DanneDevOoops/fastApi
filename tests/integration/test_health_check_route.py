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


def test_app_healt_check(client, health_headers) -> None:
    response = client.get("/api/utils/health_check", headers=health_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == "Server is OK"
