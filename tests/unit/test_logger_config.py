#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import logging
from types import SimpleNamespace

import pytest

import src.core.logger_config as logger_config

pytestmark = pytest.mark.unit


def _fake_settings(log_dir: str, logger_name: str = "test_logger") -> SimpleNamespace:
    return SimpleNamespace(
        app_logger_name=logger_name,
        file_logger_dir=log_dir,
        file_logger_file_name="test.log",
        file_logger_level="INFO",
        file_logger_mode="w",
        console_logger_level="DEBUG",
    )


def test_init_logger_returns_logger_instance(monkeypatch, tmp_path):
    monkeypatch.setattr(
        logger_config, "get_settings", lambda: _fake_settings(str(tmp_path / "logs"))
    )

    result = logger_config.init_logger()

    assert isinstance(result, logging.Logger)


def test_init_logger_uses_settings_logger_name(monkeypatch, tmp_path):
    monkeypatch.setattr(
        logger_config,
        "get_settings",
        lambda: _fake_settings(str(tmp_path / "logs"), "my_app_logger"),
    )

    result = logger_config.init_logger()

    assert result.name == "my_app_logger"


def test_init_logger_creates_log_directory(monkeypatch, tmp_path):
    log_dir = tmp_path / "new_log_dir"
    assert not log_dir.exists()

    monkeypatch.setattr(
        logger_config, "get_settings", lambda: _fake_settings(str(log_dir))
    )

    logger_config.init_logger()

    assert log_dir.exists()


def test_init_logger_falls_back_to_input_name_when_settings_name_is_empty(
    monkeypatch, tmp_path
):
    settings = _fake_settings(str(tmp_path / "logs"), logger_name=None)
    monkeypatch.setattr(logger_config, "get_settings", lambda: settings)

    result = logger_config.init_logger("fallback_logger")

    assert isinstance(result, logging.Logger)
    assert result.name == "fallback_logger"


def test_init_logger_falls_back_to_default_name_when_both_are_none(
    monkeypatch, tmp_path
):
    settings = _fake_settings(str(tmp_path / "logs"), logger_name=None)
    monkeypatch.setattr(logger_config, "get_settings", lambda: settings)

    result = logger_config.init_logger()

    assert isinstance(result, logging.Logger)
    assert result.name == "application_logger"
