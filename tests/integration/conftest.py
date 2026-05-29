#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

"""Integration test fixtures - Database setup/teardown for integration tests only"""

import asyncio

import pytest

from src.db.config.base import Base
from src.db.connectors.sqlite_db import SQLiteConnector

TEST_DB_URL = "sqlite:///src/db/test_data_storage.db"
sqlite_connector = SQLiteConnector(TEST_DB_URL)


async def _create_tables():
    async with sqlite_connector.sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _drop_tables():
    async with sqlite_connector.sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
def sqlite_schema():
    """
    Database setup/teardown for integration tests.

    This fixture is autouse=True ONLY for integration tests because it's
    in tests/integration/conftest.py. Unit tests in tests/unit/ will NOT
    use this fixture.
    """
    asyncio.run(_create_tables())
    yield
    asyncio.run(_drop_tables())
