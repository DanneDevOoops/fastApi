#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

"""
Tests for gzip response middleware.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.middlewares.gzip import GzipResponseMiddleware

pytestmark = pytest.mark.unit


def create_test_app() -> FastAPI:
    """
    Create a lightweight FastAPI app configured with gzip middleware for tests.
    """
    app = FastAPI()
    app.add_middleware(GzipResponseMiddleware, minimum_size=100, compresslevel=9)

    @app.get("/large")
    async def large_payload():
        return {"payload": "x" * 2000}

    return app


def test_gzip_compresses_large_response():
    """
    Ensure large responses are compressed when client accepts gzip.
    """
    client = TestClient(create_test_app())
    response = client.get("/large", headers={"Accept-Encoding": "gzip"})

    assert response.status_code == 200
    assert response.headers.get("content-encoding") == "gzip"
    assert "accept-encoding" in response.headers.get("vary", "").lower()


def test_gzip_skips_when_client_does_not_accept_gzip():
    """
    Ensure response is not gzip-compressed when client does not accept it.
    """
    client = TestClient(create_test_app())
    response = client.get("/large", headers={"Accept-Encoding": "identity"})

    assert response.status_code == 200
    assert response.headers.get("content-encoding") is None
