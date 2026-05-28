#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

from src.api.v2_routes import auth_routes as v2_auth_routes
from tests.conftest import _serialize_object, build_fake_document_class


def test_v2_auth_signin_route(client, monkeypatch):
    monkeypatch.setattr(v2_auth_routes, "model_serialize", _serialize_object)
    fake_user_cls = build_fake_document_class(
        "id",
        "username",
        "email",
        "password",
        "role",
        "firstname",
        "lastname",
        "address",
        "zip_code",
        "city",
        "country",
        "phone",
        "tags",
        "index",
        "deleted_at",
    )
    user = fake_user_cls(
        id="user-v2-auth",
        username="user-v2-auth",
        email="auth@example.com",
        password="hashed-password",
        role="user",
    )
    fake_user_cls._find_one_result = user
    monkeypatch.setattr(v2_auth_routes, "User", fake_user_cls)
    monkeypatch.setattr(v2_auth_routes, "verify_password_v2", lambda plain, hashed: True)
    monkeypatch.setattr(
        v2_auth_routes,
        "create_user_access_token",
        lambda username, user_id, role: "jwt-token",
    )

    response = client.post(
        "/api/v2/auth/signin",
        json={"username": "user-v2-auth", "email": "auth@example.com", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json()["token"] == "jwt-token"
    assert response.json()["user"]["id"] == "user-v2-auth"

    fake_user_cls._find_one_result = None
    response = client.post(
        "/api/v2/auth/signin",
        json={"username": "missing", "email": "missing@example.com", "password": "password"},
    )
    assert response.status_code == 401
