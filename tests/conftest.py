#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import asyncio
import os
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.core.auth import get_api_key_v2, hash_key_v2
from src.db.config.base import Base
from src.db.connectors.postgres_db import get_pg_db
from src.db.connectors.sqlite_db import SQLiteConnector
from src.db.models.v1_models.applications_model_v1 import Application as V1Application
from src.db.models.v1_models.users_model_v1 import User as V1User
from src.main import app

TEST_DB_URL = "sqlite:///src/db/test_data_storage.db"
sqlite_connector = SQLiteConnector(TEST_DB_URL)
app.dependency_overrides[get_pg_db] = sqlite_connector.get_sqlite_db
app.dependency_overrides[get_api_key_v2] = lambda: "test-api-key"


def _serialize_object(obj):
    if obj is None:
        return None
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return {
        key: value
        for key, value in vars(obj).items()
        if not key.startswith("_") and not callable(value)
    }


class FakeQuery:
    def __init__(self, result):
        self.result = result

    def sort(self, *_args, **_kwargs):
        return self

    async def first_or_none(self):
        return self.result

    async def to_list(self):
        if self.result is None:
            return []
        return self.result if isinstance(self.result, list) else [self.result]


def build_fake_document_class(*field_names):
    class FakeDocument:
        _find_result = None
        _find_one_result = None
        _create_result = None

        def __init__(self, **kwargs):
            for field in field_names:
                setattr(self, field, kwargs.get(field))
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.save = AsyncMock(return_value=self)
            self.delete = AsyncMock(return_value=None)

        @classmethod
        def find(cls, *args, **kwargs):
            return FakeQuery(cls._find_result)

        @classmethod
        def all(cls):
            return FakeQuery(cls._find_result)

        @classmethod
        async def find_one(cls, *args, **kwargs):
            return cls._find_one_result

        async def create(self, *args, **kwargs):
            return type(self)._create_result or self

    for field in field_names:
        setattr(FakeDocument, field, field)

    return FakeDocument


async def _create_tables():
    async with sqlite_connector.sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _drop_tables():
    async with sqlite_connector.sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def sqlite_schema():
    asyncio.run(_create_tables())
    yield
    asyncio.run(_drop_tables())


@pytest.fixture(scope="function")
def health_headers():
    os.environ["APP_HEALTH_CHECK_API_KEY"] = os.getenv(
        "APP_HEALTH_CHECK_API_KEY"
    ) or "your-secret-test-api-key"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-Key": os.getenv("APP_HEALTH_CHECK_API_KEY"),
    }
    yield headers
    if os.getenv("APP_HEALTH_CHECK_API_KEY") == "your-secret-test-api-key":
        del os.environ["APP_HEALTH_CHECK_API_KEY"]


async def _insert_v1_application(**overrides):
    async with sqlite_connector.async_session_local() as db:
        app_obj = V1Application(
            id=overrides.get("id", "app-1"),
            name=overrides.get("name", "app-1"),
            description=overrides.get("description", "app desc"),
            url=overrides.get("url", "http://localhost:9000"),
            is_active=overrides.get("is_active", True),
            api_key=overrides.get("api_key", hash_key_v2("app-key")),
            created_at=overrides.get("created_at", datetime.now(timezone.utc)),
            updated_at=overrides.get("updated_at", datetime.now(timezone.utc)),
            deleted_at=overrides.get("deleted_at"),
        )
        db.add(app_obj)
        await db.commit()
        await db.refresh(app_obj)
        return app_obj


async def _insert_v1_user(**overrides):
    async with sqlite_connector.async_session_local() as db:
        user_obj = V1User(
            id=overrides.get("id", "user-1"),
            username=overrides.get("username", "user-1"),
            email=overrides.get("email", f"{overrides.get('id', 'user-1')}@example.com"),
            password=overrides.get("password", hash_key_v2("password")),
            first_name=overrides.get("first_name", "User"),
            last_name=overrides.get("last_name", "One"),
            phone_number=overrides.get("phone_number", "1234567890"),
            address=overrides.get("address", "Main Street 1"),
            city=overrides.get("city", "City"),
            state=overrides.get("state", "State"),
            country=overrides.get("country", "Country"),
            zip_code=overrides.get("zip_code", "12345"),
            is_active=overrides.get("is_active", True),
            is_superuser=overrides.get("is_superuser", False),
            created_at=overrides.get("created_at", datetime.now(timezone.utc)),
            updated_at=overrides.get("updated_at", datetime.now(timezone.utc)),
            deleted_at=overrides.get("deleted_at"),
        )
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
        return user_obj
