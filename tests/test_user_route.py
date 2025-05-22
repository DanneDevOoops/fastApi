#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Test suit for the User routes in the FastAPI application.
"""

import os

import pytest
from fastapi.testclient import TestClient

from src.db.config.base import Base
from src.db.connectors.postgres_db import get_pg_db
from src.db.connectors.sqlite_db import SQLiteConnector
from src.main import app


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


# Ensure the directory exists
os.makedirs(os.path.dirname("src/db/test_data_storage.db"), exist_ok=True)

# Initialize SQLiteConnector
TEST_DB_URL = "sqlite:///src/db/test_data_storage.db"
sqlite_connector = SQLiteConnector(TEST_DB_URL)

# Override the get_pg_db dependency
app.dependency_overrides[get_pg_db] = sqlite_connector.get_sqlite_db
client = TestClient(app)


def setup():
    """
    Creates all the database tables.
    """
    Base.metadata.create_all(sqlite_connector.sqlite_engine)


def teardown():
    """
    Drop all the database tables.
    """
    Base.metadata.drop_all(sqlite_connector.sqlite_engine)


def test_users_options_route(setup_request_headers) -> None:
    """
    Test the options endpoint of the FastAPI application.
    """
    response = client.options("/api/v1/users", headers=setup_request_headers)

    assert response.status_code == 204
    assert response.headers["allow"] == "GET, POST, PUT, PATCH, DELETE"
    assert response.content == b""

# def test_read_users(setup_request_headers) -> None:
#     """
#     Test the GET endpoint of the /users route.
#     """
#     response = client.get("/api/v1/users", headers=setup_request_headers)
#
#     assert response.status_code == 200
#     assert response.json() == []
