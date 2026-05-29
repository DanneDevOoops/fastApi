#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest

from src.core.cors_config import cors_config

pytestmark = pytest.mark.unit


def test_cors_config_has_required_keys():
    assert "allowed_origins" in cors_config
    assert "allowed_credentials" in cors_config
    assert "allowed_methods" in cors_config
    assert "allowed_headers" in cors_config


def test_cors_config_allows_all_origins():
    assert "*" in cors_config["allowed_origins"]


def test_cors_config_allows_standard_methods():
    methods = cors_config["allowed_methods"]

    assert "GET" in methods
    assert "POST" in methods
    assert "PUT" in methods
    assert "PATCH" in methods
    assert "DELETE" in methods
    assert "OPTIONS" in methods


def test_cors_config_allows_api_key_header():
    assert "x-api-key" in cors_config["allowed_headers"]


def test_cors_config_credentials_is_bool():
    assert isinstance(cors_config["allowed_credentials"], bool)
