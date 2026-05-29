#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import json
from datetime import datetime
from typing import Optional

import pytest
from pydantic import ValidationError

from src.db.schemas.v1_schemas.application_schemas import (
    ApplicationCreate,
    ApplicationOutput,
    ApplicationUpdate,
)
from src.db.schemas.v1_schemas.user_schemas import (
    UserCreate,
    UserOutput,
    UserSimple,
    UserUpdate,
)

pytestmark = pytest.mark.unit


# ──────────────────────────────── helpers ────────────────────────────────────

_NOW = datetime(2024, 6, 1, 10, 0, 0)


def _make_application_output(**overrides) -> ApplicationOutput:
    defaults = dict(
        id="app-1",
        name="My App",
        description="An application",
        url="http://example.com",
        is_active=True,
        created_at=_NOW,
        updated_at=_NOW,
    )
    defaults.update(overrides)
    return ApplicationOutput(**defaults)


def _make_user_output(**overrides) -> UserOutput:
    defaults = dict(
        id="user-1",
        username="alice",
        email="alice@example.com",
        password="secret",
        first_name="Alice",
        last_name="Smith",
        phone_number="555-1234",
        address="123 Main St",
        city="Springfield",
        state="IL",
        country="US",
        zip_code="62701",
        is_active=True,
        is_superuser=False,
        created_at=_NOW,
        updated_at=_NOW,
    )
    defaults.update(overrides)
    return UserOutput(**defaults)


# ──────────────────────────── ApplicationCreate ───────────────────────────────


def test_application_create_auto_generates_id():
    app = ApplicationCreate(name="svc", description="desc", url="http://x.com")

    assert isinstance(app.id, str)
    assert len(app.id) > 0


def test_application_create_explicit_id():
    app = ApplicationCreate(
        id="my-id", name="svc", description="desc", url="http://x.com"
    )

    assert app.id == "my-id"


def test_application_create_defaults():
    app = ApplicationCreate(name="svc", description="desc", url="http://x.com")

    assert app.is_active is True


def test_application_create_rejects_empty_name():
    with pytest.raises(ValidationError):
        ApplicationCreate(name="", description="desc", url="http://x.com")


# ──────────────────────────── ApplicationUpdate ───────────────────────────────


def test_application_update_all_none_by_default():
    update = ApplicationUpdate()

    assert update.name is None
    assert update.description is None
    assert update.url is None
    assert update.is_active is None


def test_application_update_partial_fields():
    update = ApplicationUpdate(name="New Name")

    assert update.name == "New Name"
    assert update.description is None


def test_application_update_rejects_empty_string_name():
    with pytest.raises(ValidationError):
        ApplicationUpdate(name="")


# ──────────────────────────── ApplicationOutput ───────────────────────────────


def test_application_output_serialize_datetime_to_timestamp():
    app = _make_application_output()
    data = app.model_dump()

    assert data["created_at"] == _NOW.timestamp()
    assert data["updated_at"] == _NOW.timestamp()


def test_application_output_serialize_deleted_at_none():
    app = _make_application_output(deleted_at=None)
    data = app.model_dump()

    assert data["deleted_at"] is None


def test_application_output_serialize_deleted_at_with_value():
    app = _make_application_output(deleted_at=_NOW)
    data = app.model_dump()

    assert data["deleted_at"] == _NOW.timestamp()


def test_application_output_str_returns_valid_json():
    app = _make_application_output()
    result = str(app)
    parsed = json.loads(result)

    assert parsed["id"] == "app-1"
    assert parsed["name"] == "My App"


def test_application_output_equality():
    app_a = _make_application_output()
    app_b = _make_application_output()

    assert app_a == app_b


def test_application_output_inequality():
    app_a = _make_application_output()
    app_b = _make_application_output(name="Other App")

    assert app_a != app_b
    assert not (app_a == app_b)


def test_application_output_not_equal_to_non_instance():
    app = _make_application_output()

    assert app != "not an ApplicationOutput"
    assert not (app == 42)


def test_application_output_as_named_tuple():
    app = _make_application_output()
    nt = app.as_named_tuple()

    assert nt.id == "app-1"
    assert nt.name == "My App"
    assert nt.is_active is True


# ──────────────────────────────── UserCreate ─────────────────────────────────


def test_user_create_defaults_timestamps():
    user = UserCreate(
        username="bob",
        email="bob@example.com",
        password="pass",
        first_name="Bob",
        last_name="Jones",
        phone_number="555-0000",
        address="1 St",
        city="City",
        state="ST",
        country="US",
        zip_code="00000",
    )

    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert user.deleted_at is None
    assert user.is_active is True
    assert user.is_superuser is False


def test_user_create_auto_generates_id():
    user = UserCreate(
        username="bob",
        email="b@b.com",
        password="pw",
        first_name="Bob",
        last_name="Jones",
        phone_number="555",
        address="addr",
        city="city",
        state="ST",
        country="US",
        zip_code="00000",
    )

    assert isinstance(user.id, str)
    assert len(user.id) > 0


# ──────────────────────────────── UserUpdate ─────────────────────────────────


def test_user_update_all_none_by_default():
    update = UserUpdate()

    assert update.username is None
    assert update.email is None
    assert update.password is None
    assert update.is_active is None


def test_user_update_partial_fields():
    update = UserUpdate(username="charlie", email="charlie@example.com")

    assert update.username == "charlie"
    assert update.password is None


# ──────────────────────────────── UserSimple ─────────────────────────────────


def test_user_simple_required_fields():
    user = UserSimple(
        id="u-1",
        username="alice",
        email="alice@example.com",
        first_name="Alice",
        last_name="Smith",
    )

    assert user.id == "u-1"
    assert user.username == "alice"


def test_user_simple_rejects_missing_fields():
    with pytest.raises(ValidationError):
        UserSimple(id="u-1", username="alice")


# ──────────────────────────────── UserOutput ─────────────────────────────────


def test_user_output_str_returns_valid_json():
    user = _make_user_output()
    result = str(user)
    parsed = json.loads(result)

    assert parsed["id"] == "user-1"
    assert parsed["username"] == "alice"


def test_user_output_equality():
    user_a = _make_user_output()
    user_b = _make_user_output()

    assert user_a == user_b


def test_user_output_inequality():
    user_a = _make_user_output()
    user_b = _make_user_output(username="bob")

    assert user_a != user_b


def test_user_output_as_named_tuple():
    user = _make_user_output()
    nt = user.as_named_tuple()

    assert nt.id == "user-1"
    assert nt.username == "alice"
    assert nt.email == "alice@example.com"
