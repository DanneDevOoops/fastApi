#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Exception handlers module for the FastAPI application.
"""

import logging

from fastapi import HTTPException, Request

from src.core.custom_exceptions import (
    AuthException,
    BadRequestException,
    ConflictException,
    DatabaseException,
    InternalServerException,
    NotFoundException,
    ValidationException,
)
from src.core.env_config import get_settings
from src.core.responses import AppJSONResponse

settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")


async def auth_exception_handler(
    _request: Request, exc: AuthException
) -> AppJSONResponse:
    """
    Exception handler for AuthException exceptions.
    """
    logger.debug("AuthException: %s", exc)
    return AppJSONResponse(status_code=exc.status_code, content={"message": exc.detail})


async def bad_request_exception_handler(
    _request: Request, exc: BadRequestException
) -> AppJSONResponse:
    """
    Exception handler for BadRequestException exceptions.
    """
    logger.debug("BadRequestException: %s", exc)
    return AppJSONResponse(status_code=exc.status_code, content={"message": exc.detail})


async def conflict_exception_handler(
    _request: Request, exc: ConflictException
) -> AppJSONResponse:
    """
    Exception handler for ConflictException exceptions.
    """
    logger.debug("ConflictException: %s", exc)
    return AppJSONResponse(status_code=exc.status_code, content={"message": exc.detail})


async def database_exception_handler(
    _request: Request, exc: DatabaseException
) -> AppJSONResponse:
    """
    Exception handler for DatabaseException exceptions.
    """
    logger.debug("DatabaseException: %s", exc)
    return AppJSONResponse(status_code=exc.status_code, content={"message": exc.detail})


async def internal_server_exception_handler(
    _request: Request, exc: InternalServerException
) -> AppJSONResponse:
    """
    Exception handler for InternalServerException exceptions.
    """
    logger.debug("InternalServerException: %s", exc)
    return AppJSONResponse(status_code=exc.status_code, content={"message": exc.detail})


async def not_found_exception_handler(
    _request: Request, exc: NotFoundException
) -> AppJSONResponse:
    """
    Exception handler for NotFoundException exceptions.
    """
    logger.debug("NotFoundException: %s", exc)
    return AppJSONResponse(status_code=exc.status_code, content={"message": exc.detail})


async def validation_exception_handler(
    _request: Request, exc: ValidationException
) -> AppJSONResponse:
    """
    Exception handler for ValidationException exceptions.
    """
    logger.debug("ValidationException: %s", exc)
    return AppJSONResponse(status_code=exc.status_code, content={"message": exc.detail})


async def http_exception_handler(
    _request: Request, exc: HTTPException
) -> AppJSONResponse:
    """
    Exception handler for HTTPException exceptions.
    """
    logger.debug("HTTPException: %s", exc)
    return AppJSONResponse(status_code=exc.status_code, content={"message": exc.detail})
