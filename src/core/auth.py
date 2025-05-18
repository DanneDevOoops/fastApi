#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains the authentication logic for the FastAPI application.
"""

import logging

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyQuery, APIKeyHeader

from src.core.env_config import get_settings

# Init Logger
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")


def get_auth_headers_and_query_params() -> tuple:
    """
    Create and return the authentication headers and query parameters.

    :return: A tuple containing the query API key and header API key objects.
    """
    query_api_key = APIKeyQuery(name="api_key", auto_error=False)
    header_api_key = APIKeyHeader(name="x-api-key", auto_error=False)
    return header_api_key, query_api_key


def get_allowed_api_keys(settings) -> list:
    """
    Generate a list of allowed API keys from the application settings.

    NOTE: This is where you will add any application api keys you want to use for
    authentication with the API. When an adding a new key, be sure to check the
    `src/core/env_config.py` for configured env variables before adding just anything here.

    :param settings: The application settings object.
    :return: A list of valid API keys.
    """
    return [
        key for key in [
            settings.app_health_check_api_key or None,
            settings.app_1_api_key or None,
        ] if key is not None or ''
    ]


# Auth headers & query params
ALLOWED_API_KEYS = get_allowed_api_keys(settings)
header_api_key, query_api_key = get_auth_headers_and_query_params()


async def get_api_key(
        api_key_query: str = Security(query_api_key),
        api_key_header: str = Security(header_api_key),
) -> str:
    """
    Validate the API key provided in the query parameters or headers.

    This function checks if the API key provided in the `x-api-key` header or the `api_key`
    query parameter matches any of the keys in the `ALLOWED_API_KEYS` list. If a match is
    found, the valid API key is returned. If neither matches, an HTTP 401 Unauthorized
    exception is raised.

    :param api_key_query: The API key provided in the query parameters.
    :type api_key_query: str
    :param api_key_header: The API key provided in the headers.
    :type api_key_header: str
    :return: The valid API key if authentication is successful.
    :rtype: str
    :raises HTTPException: If the API key is invalid or missing.
    """
    if api_key_header in ALLOWED_API_KEYS:
        return api_key_header
    if api_key_query in ALLOWED_API_KEYS:
        return api_key_query

    # This part only happens if the API key is not found in the allowed keys to trigger
    # the warning log and raise an HTTPException return.
    logger.warning('API key not found or invalid', extra={
        'api_key_query': api_key_query,
        'api_key_header': api_key_header
    })

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
