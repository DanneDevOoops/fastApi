#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Test suit for the Health Check route in the FastAPI application.
"""

import os

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_request_headers():
    """
    Fixture to set up request headers for the test client.
    """
    # Setup: Set the environment variable
    os.environ["APP_HEALTH_CHECK_API_KEY"] = os.getenv(
        "APP_HEALTH_CHECK_API_KEY") or "your-secret-test-api-key"
    request_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-Key": os.getenv("APP_HEALTH_CHECK_API_KEY")
    }
    yield request_headers
    # Teardown: Remove the environment variable
    if os.getenv("APP_HEALTH_CHECK_API_KEY") == "your-secret-test-api-key":
        del os.environ["APP_HEALTH_CHECK_API_KEY"]
        print("Environment variable APP_HEALTH_CHECK_API_KEY deleted")


def test_app_health_check(setup_request_headers) -> None:
    """
    Test the health check endpoint of the FastAPI application.
    """
    response = client.get("/api/utils/health_check",
                          headers=setup_request_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == "Server is OK"


def test_app_healt_check(setup_request_headers) -> None:
    """
    Test the health check endpoint of the FastAPI application.
    """
    response = client.get("/api/utils/health_check",
                          headers=setup_request_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == "Server is OK"
