#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import asyncio
import json

import pytest

from src.core import exception_handlers as handlers
from src.core.custom_exceptions import (
    AuthException,
    BadRequestException,
    ConflictException,
    DatabaseException,
)
from src.core.custom_exceptions import HTTPException as CustomHTTPException
from src.core.custom_exceptions import (
    InternalServerException,
    NotFoundException,
    ValidationException,
)

pytestmark = pytest.mark.unit


def _payload(response):
    return json.loads(response.body)


@pytest.mark.parametrize(
    ("handler", "exception", "status_code"),
    [
        (handlers.auth_exception_handler, AuthException("auth"), 401),
        (handlers.bad_request_exception_handler, BadRequestException("bad"), 400),
        (handlers.conflict_exception_handler, ConflictException("conflict"), 409),
        (handlers.database_exception_handler, DatabaseException("db"), 500),
        (
            handlers.internal_server_exception_handler,
            InternalServerException("internal"),
            500,
        ),
        (handlers.not_found_exception_handler, NotFoundException("missing"), 404),
        (handlers.validation_exception_handler, ValidationException("invalid"), 422),
        (handlers.http_exception_handler, CustomHTTPException("http"), 500),
    ],
)
def test_exception_handlers(handler, exception, status_code):
    response = asyncio.run(asyncio_call(handler, exception))
    assert response.status_code == status_code
    assert _payload(response) == {"message": exception.detail}


def asyncio_call(handler, exception):
    async def _run():
        return await handler(None, exception)

    return _run()


def test_http_exception_handler_handles_fastapi_http_exception():
    from fastapi import HTTPException

    response = asyncio.run(
        asyncio_call(
            handlers.http_exception_handler,
            HTTPException(status_code=418, detail="teapot"),
        )
    )
    assert response.status_code == 418
    assert _payload(response) == {"message": "teapot"}
