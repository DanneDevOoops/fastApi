#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from fastapi import Request

import pytest
from fastapi import HTTPException
from jose import JWTError

from src.core import auth

pytestmark = pytest.mark.unit


def test_hash_and_verify_password_roundtrip():
    hashed = auth.hash_key_v2("secret-password")

    assert hashed != "secret-password"
    assert auth.verify_password_v2("secret-password", hashed) is True
    assert auth.verify_password_v2("wrong-password", hashed) is False
    assert auth.verify_password_v2("secret-password", "") is False
    assert auth.verify_password_v2("secret-password", "not-a-bcrypt-hash") is False


def test_application_token_helpers(monkeypatch):
    monkeypatch.setattr(auth.settings, "app_jwt_secret_key", "unit-secret")
    monkeypatch.setattr(auth.settings, "app_jwt_algorithm", "HS256")

    token = auth.create_application_access_token("app-name", "app-id")
    payload = auth.decode_application_access_token(token)

    assert payload["sub"] == "app-name"
    assert payload["id"] == "app-id"


def test_get_supplied_api_key_prefers_header():
    assert auth._get_supplied_api_key("header-key", "query-key") == "header-key"
    assert auth._get_supplied_api_key(None, "query-key") == "query-key"

    with pytest.raises(HTTPException):
        auth._get_supplied_api_key(None, None)


def test_build_application_api_credentials(monkeypatch):
    monkeypatch.setattr(
        auth, "create_application_access_token", lambda **kwargs: "raw-token"
    )
    monkeypatch.setattr(auth, "hash_key_v2", lambda value: f"hashed:{value}")

    raw_token, hashed_token = auth.build_application_api_credentials("app", "id")

    assert raw_token == "raw-token"
    assert hashed_token == "hashed:raw-token"


def test_get_current_user(monkeypatch):
    monkeypatch.setattr(
        auth.jwt, "decode", lambda *args, **kwargs: {"sub": "user", "id": "123"}
    )

    assert asyncio.run(auth.get_current_user("token")) == {
        "username": "user",
        "id": "123",
    }

    def raise_jwt_error(*_args, **_kwargs):
        raise JWTError("bad-token")

    monkeypatch.setattr(auth.jwt, "decode", raise_jwt_error)
    with pytest.raises(HTTPException):
        asyncio.run(auth.get_current_user("token"))


def test_get_api_key_v1(monkeypatch):
    raw_token = "raw-token"
    monkeypatch.setattr(
        auth, "decode_application_access_token", lambda value: {"id": "app-id"}
    )
    monkeypatch.setattr(
        auth,
        "verify_password_v2",
        lambda raw, hashed: raw == raw_token and hashed == "hashed-token",
    )

    class FakeResult:
        def scalar_one_or_none(self):
            return SimpleNamespace(api_key="hashed-token")

    class FakeDb:
        async def execute(self, _stmt):
            return FakeResult()

    mock_request = MagicMock(spec=Request)
    mock_request.method = "GET"

    assert (
        asyncio.run(auth.get_api_key_v1(request=mock_request, api_key_header=raw_token, db=FakeDb()))
        == raw_token
    )


def test_get_auth_headers_and_query_params():
    from fastapi.security import APIKeyHeader, APIKeyQuery

    header_key, query_key = auth.get_auth_headers_and_query_params()

    assert isinstance(header_key, APIKeyHeader)
    assert isinstance(query_key, APIKeyQuery)


def test_create_user_access_token(monkeypatch):
    from jose import jwt as jose_jwt

    monkeypatch.setattr(auth.settings, "app_jwt_secret_key", "unit-secret")
    monkeypatch.setattr(auth.settings, "app_jwt_algorithm", "HS256")

    token = auth.create_user_access_token("alice", "user-1", "admin", expires_in_sec=60)
    payload = jose_jwt.decode(token, "unit-secret", algorithms=["HS256"])

    assert payload["sub"] == "alice"
    assert payload["id"] == "user-1"
    assert payload["role"] == "admin"
    assert "exp" in payload
    assert "iat" in payload


def test_decode_application_access_token_raises_on_invalid_token():
    with pytest.raises(HTTPException):
        auth.decode_application_access_token("not-a-valid-jwt-token")


def test_get_health_check_api_key_accepts_valid_key(monkeypatch):
    monkeypatch.setenv("APP_HEALTH_CHECK_API_KEY", "expected-key")
    monkeypatch.setattr(auth.settings, "app_health_check_api_key", "expected-key")

    result = asyncio.run(
        auth.get_health_check_api_key(api_key_query=None, api_key_header="expected-key")
    )

    assert result == "expected-key"


def test_get_health_check_api_key_rejects_wrong_key(monkeypatch):
    monkeypatch.setenv("APP_HEALTH_CHECK_API_KEY", "expected-key")
    monkeypatch.setattr(auth.settings, "app_health_check_api_key", "expected-key")

    with pytest.raises(HTTPException):
        asyncio.run(
            auth.get_health_check_api_key(
                api_key_query=None, api_key_header="wrong-key"
            )
        )


def test_get_health_check_api_key_rejects_when_no_expected_key_configured(monkeypatch):
    monkeypatch.delenv("APP_HEALTH_CHECK_API_KEY", raising=False)
    monkeypatch.setattr(auth.settings, "app_health_check_api_key", None)

    with pytest.raises(HTTPException):
        asyncio.run(
            auth.get_health_check_api_key(api_key_query=None, api_key_header="any-key")
        )


def test_get_api_key_v2(monkeypatch):
    raw_token = "raw-token"
    monkeypatch.setattr(
        auth, "decode_application_access_token", lambda value: {"id": "app-id"}
    )
    monkeypatch.setattr(
        auth,
        "verify_password_v2",
        lambda raw, hashed: raw == raw_token and hashed == "hashed-token",
    )

    # Create a mock class with field descriptors that support comparison operations
    class MockApplicationV2:
        class FieldDescriptor:
            def __eq__(self, other):
                return True

            def __ne__(self, other):
                return False

        id = FieldDescriptor()
        deleted_at = FieldDescriptor()

        @staticmethod
        async def find_one(*args, **kwargs):
            return SimpleNamespace(api_key="hashed-token")

    monkeypatch.setattr(auth, "ApplicationV2", MockApplicationV2)

    mock_request = MagicMock(spec=Request)
    mock_request.method = "GET"

    assert asyncio.run(auth.get_api_key_v2(request=mock_request, api_key_header=raw_token)) == raw_token
