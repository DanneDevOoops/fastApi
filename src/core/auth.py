#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains the authentication logic for the FastAPI application.
"""

import logging
import os

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyQuery, APIKeyHeader

from src.core.env_config import get_settings

# Init Logger
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")

# Auth headers & query params
query_api_key = APIKeyQuery(name="api_key", auto_error=False)
header_api_key = APIKeyHeader(name="x-api-key", auto_error=False)

# Allowed API keys for authentication of applications accessing the API
API_KEYS = [
    os.getenv("APP_HEALTH_API_KEY", None),
    os.getenv("APP_1_API_KEY", None)
]


async def get_api_key(
        api_key_query: str = Security(query_api_key),
        api_key_header: str = Security(header_api_key),
) -> str:
    """
    Validate the API key provided in the query parameters or headers.

    This function checks if the API key provided in the query parameters or
    headers matches any of the predefined API keys. If a valid API key is
    found, it is returned. Otherwise, an HTTP 401 Unauthorized exception is
    raised.

    :param api_key_query: The API key provided in the query parameters.
    :type api_key_query: str
    :param api_key_header: The API key provided in the headers.
    :type api_key_header: str
    :return: The valid API key.
    :rtype: str
    :raises HTTPException: If the API key is invalid or missing.
    """
    if api_key_query in API_KEYS:
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header

    logger.warning('API key not found or invalid', extra={
        'api_key_query': api_key_query,
        'api_key_header': api_key_header
    })

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
