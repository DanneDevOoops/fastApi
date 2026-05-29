#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import logging
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import src.middlewares.logger as logger_middleware_module
from src.middlewares.logger import LoggerMiddleware

pytestmark = pytest.mark.unit


def _build_app(mock_logger: MagicMock) -> FastAPI:
    app = FastAPI()
    app.add_middleware(LoggerMiddleware)

    @app.get("/ping")
    async def ping():
        return {"pong": True}

    return app


def test_logger_middleware_passes_request_through(monkeypatch):
    mock_logger = MagicMock(spec=logging.Logger)
    monkeypatch.setattr(
        logger_middleware_module, "init_logger", lambda name: mock_logger
    )

    client = TestClient(_build_app(mock_logger))
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_logger_middleware_logs_request_details(monkeypatch):
    mock_logger = MagicMock(spec=logging.Logger)
    monkeypatch.setattr(
        logger_middleware_module, "init_logger", lambda name: mock_logger
    )

    client = TestClient(_build_app(mock_logger))
    client.get("/ping")

    logged_messages = [call.args[0] for call in mock_logger.info.call_args_list]
    assert any("Request details" in msg for msg in logged_messages)


def test_logger_middleware_logs_response_details(monkeypatch):
    mock_logger = MagicMock(spec=logging.Logger)
    monkeypatch.setattr(
        logger_middleware_module, "init_logger", lambda name: mock_logger
    )

    client = TestClient(_build_app(mock_logger))
    client.get("/ping")

    logged_messages = [call.args[0] for call in mock_logger.info.call_args_list]
    assert any("Response details" in msg for msg in logged_messages)


def test_logger_middleware_calls_info_at_least_twice(monkeypatch):
    mock_logger = MagicMock(spec=logging.Logger)
    monkeypatch.setattr(
        logger_middleware_module, "init_logger", lambda name: mock_logger
    )

    client = TestClient(_build_app(mock_logger))
    client.get("/ping")

    assert mock_logger.info.call_count >= 2
