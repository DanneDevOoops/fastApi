#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest

from src.utils.app_constants import REQUEST_HEADERS, REQUEST_METHODS, REQUEST_ORIGINS

pytestmark = pytest.mark.unit


def test_request_headers_contains_core_values():
    assert "Content-Type" in REQUEST_HEADERS
    assert "Authorization" in REQUEST_HEADERS
    assert "X-API-Key" in REQUEST_HEADERS
    assert "Accept" in REQUEST_HEADERS


def test_request_methods_contains_standard_verbs():
    assert "GET" in REQUEST_METHODS
    assert "POST" in REQUEST_METHODS
    assert "PUT" in REQUEST_METHODS
    assert "PATCH" in REQUEST_METHODS
    assert "DELETE" in REQUEST_METHODS
    assert "OPTIONS" in REQUEST_METHODS


def test_request_origins_contains_wildcard():
    assert "*" in REQUEST_ORIGINS


def test_request_constants_are_lists():
    assert isinstance(REQUEST_HEADERS, list)
    assert isinstance(REQUEST_METHODS, list)
    assert isinstance(REQUEST_ORIGINS, list)
