#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest

import src.utils.generate_v1_application_auth as gen_module
from src.utils.generate_v1_application_auth import main, parse_args

pytestmark = pytest.mark.unit


def test_parse_args_required_fields(monkeypatch):
    monkeypatch.setattr(
        "sys.argv", ["script", "--app-id", "abc123", "--app-name", "myapp"]
    )

    args = parse_args()

    assert args.app_id == "abc123"
    assert args.app_name == "myapp"


def test_parse_args_default_base_url(monkeypatch):
    monkeypatch.setattr(
        "sys.argv", ["script", "--app-id", "id1", "--app-name", "name1"]
    )

    args = parse_args()

    assert args.base_url == "http://127.0.0.1:8000"


def test_parse_args_custom_base_url(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "script",
            "--app-id",
            "id1",
            "--app-name",
            "name1",
            "--base-url",
            "https://api.example.com",
        ],
    )

    args = parse_args()

    assert args.base_url == "https://api.example.com"


def test_main_prints_raw_jwt(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv", ["script", "--app-id", "abc123", "--app-name", "myapp"]
    )
    monkeypatch.setattr(
        gen_module,
        "build_application_api_credentials",
        lambda app_name, app_id: ("raw-jwt-token", "hashed-api-key"),
    )

    main()

    output = capsys.readouterr().out
    assert "raw-jwt-token" in output


def test_main_prints_hashed_key(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv", ["script", "--app-id", "abc123", "--app-name", "myapp"]
    )
    monkeypatch.setattr(
        gen_module,
        "build_application_api_credentials",
        lambda app_name, app_id: ("raw-jwt-token", "hashed-api-key"),
    )

    main()

    output = capsys.readouterr().out
    assert "hashed-api-key" in output


def test_main_prints_app_id_in_sql(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv", ["script", "--app-id", "abc123", "--app-name", "myapp"]
    )
    monkeypatch.setattr(
        gen_module,
        "build_application_api_credentials",
        lambda app_name, app_id: ("raw-jwt-token", "hashed-api-key"),
    )

    main()

    output = capsys.readouterr().out
    assert "abc123" in output
    assert "SQL_UPDATE=" in output


def test_main_prints_section_headers(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["script", "--app-id", "id1", "--app-name", "svc"])
    monkeypatch.setattr(
        gen_module,
        "build_application_api_credentials",
        lambda app_name, app_id: ("tok", "hash"),
    )

    main()

    output = capsys.readouterr().out
    assert "RAW_JWT_USE_THIS_IN_X_API_KEY=" in output
    assert "HASHED_API_KEY_STORE_THIS_IN_POSTGRES=" in output
    assert "TEST_COMMAND=" in output


def test_main_uses_custom_base_url_in_curl(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        [
            "script",
            "--app-id",
            "id1",
            "--app-name",
            "svc",
            "--base-url",
            "https://my.api",
        ],
    )
    monkeypatch.setattr(
        gen_module,
        "build_application_api_credentials",
        lambda app_name, app_id: ("tok", "hash"),
    )

    main()

    output = capsys.readouterr().out
    assert "https://my.api" in output
