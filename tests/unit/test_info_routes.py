#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import asyncio
import json

import pytest

import src.api.health_check_routes.check_routes as check_routes_module
import src.api.health_check_routes.info_routes as info_routes_module

pytestmark = pytest.mark.unit


def test_health_check_returns_200():
    response = asyncio.run(check_routes_module.health_check())

    assert response.status_code == 200


def test_health_check_returns_ok_message():
    response = asyncio.run(check_routes_module.health_check())

    assert json.loads(response.body) == "Server is OK"


def test_info_returns_200(monkeypatch):
    monkeypatch.setattr(info_routes_module.settings, "app_name", "Test App")
    monkeypatch.setattr(info_routes_module.settings, "pyenv_version", "3.11.0")
    monkeypatch.setattr(info_routes_module.settings, "env_name", "test")

    response = asyncio.run(info_routes_module.info())

    assert response.status_code == 200


def test_info_response_contains_app_name(monkeypatch):
    monkeypatch.setattr(info_routes_module.settings, "app_name", "MyService")
    monkeypatch.setattr(info_routes_module.settings, "pyenv_version", "3.11.0")
    monkeypatch.setattr(info_routes_module.settings, "env_name", "staging")

    response = asyncio.run(info_routes_module.info())
    data = json.loads(response.body)

    assert data["name"] == "MyService"
    assert data["environment"] == "staging"
    assert "description" in data


def test_pgsql_db_info_returns_200(monkeypatch):
    monkeypatch.setattr(info_routes_module.settings, "pg_db_name", "my_postgres_db")
    monkeypatch.setattr(info_routes_module.settings, "pyenv_version", "3.11.0")
    monkeypatch.setattr(info_routes_module.settings, "env_name", "test")

    response = asyncio.run(info_routes_module.pgsql_db_info())

    assert response.status_code == 200


def test_pgsql_db_info_response_contains_db_name(monkeypatch):
    monkeypatch.setattr(info_routes_module.settings, "pg_db_name", "mydb")
    monkeypatch.setattr(info_routes_module.settings, "pyenv_version", "3.11.0")
    monkeypatch.setattr(info_routes_module.settings, "env_name", "test")

    response = asyncio.run(info_routes_module.pgsql_db_info())
    data = json.loads(response.body)

    assert data["name"] == "mydb"


def test_mongo_db_info_returns_200(monkeypatch):
    monkeypatch.setattr(info_routes_module.settings, "mongo_db_name", "my_mongo_db")
    monkeypatch.setattr(info_routes_module.settings, "pyenv_version", "3.11.0")
    monkeypatch.setattr(info_routes_module.settings, "env_name", "test")

    response = asyncio.run(info_routes_module.mongo_db_info())

    assert response.status_code == 200


def test_mongo_db_info_response_contains_db_name(monkeypatch):
    monkeypatch.setattr(info_routes_module.settings, "mongo_db_name", "sensor_data")
    monkeypatch.setattr(info_routes_module.settings, "pyenv_version", "3.11.0")
    monkeypatch.setattr(info_routes_module.settings, "env_name", "test")

    response = asyncio.run(info_routes_module.mongo_db_info())
    data = json.loads(response.body)

    assert data["name"] == "sensor_data"
