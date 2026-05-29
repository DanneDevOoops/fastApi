#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest

from src.core.env_config import get_settings

pytestmark = pytest.mark.unit


def test_get_settings_reads_environment(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Unit Test App")
    monkeypatch.setenv("NANO_ID_SIZE", "31")

    get_settings.cache_clear()
    settings = get_settings()

    assert settings.app_name == "Unit Test App"
    assert settings.nano_id_size == 31
    assert get_settings() is settings


def test_settings_default_values():
    get_settings.cache_clear()
    settings = get_settings()

    assert isinstance(settings.app_jwt_algorithm, str)
    assert len(settings.app_jwt_algorithm) > 0
    assert isinstance(settings.app_port, int)
    assert isinstance(settings.pg_db_port, int)
    assert isinstance(settings.mongo_db_port, int)
    assert isinstance(settings.nano_id_size, int)
    assert isinstance(settings.app_gzip_enabled, bool)
    assert isinstance(settings.app_debug, bool)


def test_settings_str_method():
    get_settings.cache_clear()
    settings = get_settings()

    result = str(settings)

    assert "app_name" in result
