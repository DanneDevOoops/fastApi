#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.core import app_lifespan as lifespan_module

pytestmark = pytest.mark.unit


class FakePool:
    def __init__(self, conninfo):
        self.conninfo = conninfo
        self.close = AsyncMock()


class FakeMongoConnector:
    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name
        self.db = object()
        self.close = AsyncMock()


class FakePgsqlDbSessionManager:
    def get_db_connection_str(self):
        return "postgresql://unit-test"


def test_app_lifespan_initializes_and_closes(monkeypatch):
    init_beanie = AsyncMock()
    monkeypatch.setattr(lifespan_module, "init_beanie", init_beanie)
    monkeypatch.setattr(lifespan_module, "MongoDBConnector", FakeMongoConnector)
    monkeypatch.setattr(
        lifespan_module, "PgsqlDbSessionManager", FakePgsqlDbSessionManager
    )
    monkeypatch.setattr(lifespan_module, "AsyncConnectionPool", FakePool)

    app_instance = SimpleNamespace()

    async def _run():
        async with lifespan_module.app_lifespan(app_instance):
            assert app_instance.settings is lifespan_module.settings
            assert isinstance(app_instance.mongo_connector, FakeMongoConnector)
            assert app_instance.async_pool.conninfo == "postgresql://unit-test"

    asyncio.run(_run())

    init_beanie.assert_awaited_once()
    app_instance.async_pool.close.assert_awaited_once()
    app_instance.mongo_connector.close.assert_awaited_once()
