#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Exception handlers module for the FastAPI application.
"""

import logging

from fastapi import HTTPException, Request
from fastapi.responses import ORJSONResponse

from src.core.custom_exceptions import (AuthException, BadRequestException,
                                        ConflictException, DatabaseException,
                                        InternalServerException,
                                        NotFoundException, ValidationException)
from src.core.env_config import get_settings

settings = get_settings()
logger = logging.getLogger(
    settings.app_logger_name or "application_logger")


async def auth_exception_handler(_request: Request,
                                 exc: AuthException) -> ORJSONResponse:
    """
    Exception handler for AuthException exceptions.
    """
    logger.debug("AuthException: %s", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def bad_request_exception_handler(
        _request: Request,
        exc: BadRequestException) -> ORJSONResponse:
    """
    Exception handler for BadRequestException exceptions.
    """
    logger.debug("BadRequestException: %s", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def conflict_exception_handler(_request: Request,
                                     exc: ConflictException) -> ORJSONResponse:
    """
    Exception handler for ConflictException exceptions.
    """
    logger.debug("ConflictException: %s", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def database_exception_handler(_request: Request,
                                     exc: DatabaseException) -> ORJSONResponse:
    """
    Exception handler for DatabaseException exceptions.
    """
    logger.debug("DatabaseException: %s", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def internal_server_exception_handler(
        _request: Request,
        exc: InternalServerException) -> ORJSONResponse:
    """
    Exception handler for InternalServerException exceptions.
    """
    logger.debug("InternalServerException: %s", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def not_found_exception_handler(
        _request: Request,
        exc: NotFoundException) -> ORJSONResponse:
    """
    Exception handler for NotFoundException exceptions.
    """
    logger.debug("NotFoundException: %s", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def validation_exception_handler(
        _request: Request,
        exc: ValidationException) -> ORJSONResponse:
    """
    Exception handler for ValidationException exceptions.
    """
    logger.debug("ValidationException: %s", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


async def http_exception_handler(_request: Request,
                                 exc: HTTPException) -> ORJSONResponse:
    """
    Exception handler for HTTPException exceptions.
    """
    logger.debug("HTTPException: %s", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
