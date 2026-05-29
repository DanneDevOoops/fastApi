#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest

from src.core import custom_exceptions as exc

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("exception_cls", "message", "status_code", "type_name"),
    [
        (exc.AuthException, "auth", 401, "UnauthorizedException"),
        (exc.BadRequestException, "bad-request", 400, "BadRequestException"),
        (exc.ConflictException, "conflict", 409, "ConflictException"),
        (exc.DatabaseException, "db", 500, "DatabaseException"),
        (exc.HTTPException, "http", 500, "HTTPException"),
        (exc.InternalServerException, "internal", 500, "InternalServerException"),
        (exc.NotFoundException, "missing", 404, "NotFoundException"),
        (exc.ValidationException, "invalid", 422, "ValidationException"),
    ],
)
def test_custom_exceptions(exception_cls, message, status_code, type_name):
    instance = exception_cls(message)

    assert instance.detail == message
    assert instance.status_code == status_code
    assert instance.type == type_name
    assert str(instance) == f"{type_name}: {message}"
