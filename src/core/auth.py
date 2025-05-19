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

    This function initializes and returns two objects used for API key
    authentication: one for query parameters and one for headers. These
    objects are configured to handle API key validation without raising
    automatic errors.

    :returns:
        A tuple containing:

        - **header_key** (*APIKeyHeader*): The API key object for the
          `x-api-key` header.
        - **query_key** (*APIKeyQuery*): The API key object for the
          `api_key` query parameter.

    :rtype: tuple
    """
    query_key = APIKeyQuery(name="api_key", auto_error=False)
    header_key = APIKeyHeader(name="x-api-key", auto_error=False)
    return header_key, query_key


def get_allowed_api_keys(env_settings) -> list[str]:
    """
    Generate a list of allowed API keys from the application settings.

    NOTE: This is where you will add any application api keys you want to
    use for authentication with the API. When adding a new key, be sure
    to check the `src/core/env_config.py` for configured env variables
    before adding just anything here.

    :param env_settings: The application environment settings object.
    :type env_settings: object
    :return: A list of valid API-Keys strings.
    :rtype: list[str]
    """
    return [
        key for key in [
            env_settings.app_health_check_api_key or None,
            env_settings.app_1_api_key or None,
        ] if key is not None
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

    This function checks if the API key provided in the `x-api-key` header
    or the `api_key` query parameter matches any of the keys in the
    `ALLOWED_API_KEYS` list. If a match is found, the valid API key is
    returned. If neither matches, an HTTP 401 Unauthorized exception is
    raised.

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

    # This part only happens if the API key is not found in the allowed
    # keys to trigger the warning log and raise an HTTPException return.
    logger.warning('API key not found or invalid', extra={
        'api_key_query': api_key_query,
        'api_key_header': api_key_header
    })

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
