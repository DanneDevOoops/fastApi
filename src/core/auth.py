#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=singleton-comparison


"""
This module contains the authentication logic for the FastAPI application.
"""

import logging
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.env_config import get_settings
from src.db.connectors.postgres_db import get_pg_db

# Postgres models
from src.db.models.v1_models.applications_model_v1 import \
    Application as ApplicationV1

# MongiDB models
from src.db.models.v2_models.application_model_v2 import \
    Application as ApplicationV2

settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v2/auth/token")


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


# Auth headers & query params
header_api_key, query_api_key = get_auth_headers_and_query_params()


def hash_key_v2(input_password: str) -> str:
    """
    Encrypt the input password using bcrypt hashing.

    :param input_password: The plain text password to encrypt.
    :return: The hashed password.
    :rtype: str
    """
    return bcrypt_context.hash(input_password)


def verify_password_v2(plain_password: str,
                       hashed_password: str) -> bool:
    """
    Verify if the plain password matches the hashed password.

    :param plain_password: The plain text password to verify.
    :param hashed_password: The hashed password stored in the database to
        compare against.
    :return: True if the passwords match, False otherwise.
    :rtype: bool
    """
    return bcrypt_context.verify(plain_password, hashed_password)


def create_user_access_token(
        username: str, user_id: str, user_role: str,
        expires_in_sec: int = settings.app_jwt_expiration) -> str:
    """
    Create a JWT access token for a user.

    :param username: The username to include in the token payload.
    :param user_id: The unique identifier of the user.
    :param expires_in_sec: The number of seconds until the token expires.
        This is optional and defaults to the value set in the application
        settings.
    :return: The encoded JWT access token as a string.
    :rtype: str
    """
    logger.info("Encoding %s access token for user %s",
                settings.app_jwt_token_type, user_id)
    expires_in_delta = timedelta(minutes=expires_in_sec)
    token_expires_delta = datetime.now(timezone.utc) + expires_in_delta
    encode_object = {
        "sub": username,
        "id": user_id,
        "role": user_role,
        "iat": datetime.now(timezone.utc),
        "exp": token_expires_delta
    }

    return jwt.encode(
        encode_object,
        settings.app_jwt_secret_key,
        algorithm=settings.app_jwt_algorithm
    )


async def get_current_user(
        access_token: str = Depends(oauth2_bearer)):
    """
    Retrieve the current user from the access token.
    """
    logger.info("Starting to decode access token for user credentials...")
    try:
        payload = jwt.decode(
            access_token,
            settings.app_jwt_secret_key,
            algorithms=[settings.app_jwt_algorithm])
        username = payload.get("sub")
        user_id = payload.get("id")

        # Validate that username and user_id are present in the payload
        if username is None or user_id is None:
            raise HTTPException(
                detail="Invalid authentication credentials",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return {"username": username, "id": user_id}
    except JWTError as e:
        raise HTTPException(
            detail="Invalid authentication credentials",
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from e


def create_application_access_token(
        app_name: str, app_id: str, expires_in_sec: int | None = None) -> str:
    """
    Create a JWT access token for an application or service.

    This function generates a JWT token containing the application name and ID.
    If `expires_in_sec` is provided, the token will include an expiration
    time; otherwise, the token will not expire.

    :param app_name: The name of the application to include in the token
        payload.
    :type app_name: str
    :param app_id: The unique identifier of the application.
    :type app_id: str
    :param expires_in_sec: The number of seconds until the token expires.
        If None, the token will not expire.
    :type expires_in_sec: int or None
    :return: The encoded JWT access token as a string.
    :rtype: str
    """
    logger.info("Encoding %s access token for application %s",
                settings.app_jwt_token_type, app_id)
    encode_object: dict[str, object] = {
        "sub": app_name,
        "id": app_id
    }

    if expires_in_sec is not None:
        expires_in_delta = timedelta(minutes=expires_in_sec)
        token_expires_delta = datetime.now(timezone.utc) + expires_in_delta
        encode_object["exp"] = token_expires_delta

    return jwt.encode(
        encode_object,
        settings.app_jwt_secret_key,
        algorithm=settings.app_jwt_algorithm
    )


def decode_application_access_token(
        access_token: str) -> dict:
    """
    Decode the application access token and return its payload.

    :param access_token: The JWT access token to decode.
    :return: The decoded payload of the JWT token.
    :rtype: dict
    """
    try:
        payload = jwt.decode(
            access_token,
            settings.app_jwt_secret_key,
            algorithms=[settings.app_jwt_algorithm])
        return payload
    except JWTError as e:
        raise HTTPException(
            detail="Invalid authentication credentials",
            status_code=status.HTTP_401_UNAUTHORIZED
        ) from e


def build_application_api_credentials(
        app_name: str, app_id: str,
        expires_in_sec: int | None = None) -> tuple[str, str]:
    """
    Build the raw JWT and hashed API key for an application.

    :param app_name: The application name to encode in the token.
    :param app_id: The application identifier to encode in the token.
    :param expires_in_sec: Optional expiration in minutes.
    :return: Tuple of (raw JWT token, hashed token for database storage).
    :rtype: tuple[str, str]
    """
    raw_token = create_application_access_token(
        app_name=app_name,
        app_id=app_id,
        expires_in_sec=expires_in_sec,
    )
    return raw_token, hash_key_v2(raw_token)


def _get_supplied_api_key(
        api_key_header: str | None,
        api_key_query: str | None) -> str:
    """
    Return the supplied raw API key, preferring the header value.
    """
    if api_key_header:
        return api_key_header
    if api_key_query:
        return api_key_query

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


async def get_api_key_v1(
        api_key_query: str = Security(query_api_key),
        api_key_header: str = Security(header_api_key),
        db: AsyncSession = Depends(get_pg_db),
) -> str:
    """
    Validate the API key provided in the query parameters or headers for v1
    (PostgreSQL) authentication.

    This function checks if the API key provided in the `x-api-key` header
    or the `api_key` query parameter is valid by verifying it against the
    application record stored in PostgreSQL. If a match is found, the valid
    API key is returned. If neither matches, an HTTP 401 Unauthorized
    exception is raised.

    :param api_key_query: The API key provided in the query parameters.
    :type api_key_query: str
    :param api_key_header: The API key provided in the headers.
    :type api_key_header: str
    :param db: The PostgreSQL database session.
    :type db: AsyncSession
    :return: The valid API key if authentication is successful.
    :rtype: str
    :raises HTTPException: If the API key is invalid or missing.
    """
    raw_api_key = _get_supplied_api_key(api_key_header, api_key_query)
    token_payload = decode_application_access_token(raw_api_key)

    stmt = select(ApplicationV1).where(
        ApplicationV1.id == token_payload.get("id"),
        ApplicationV1.deleted_at.is_(None),
        ApplicationV1.is_active.is_(True),
    )
    result = await db.execute(stmt)
    service_details = result.scalar_one_or_none()

    if service_details and service_details.api_key and verify_password_v2(
            raw_api_key, service_details.api_key):
        return raw_api_key

    logger.warning("Invalid Postgres API key for application id %s",
                   token_payload.get("id"))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


async def get_api_key_v2(
        api_key_query: str = Security(query_api_key),
        api_key_header: str = Security(header_api_key),
) -> str:
    """
    Validate the API key provided in the query parameters or headers for v2
    (MongoDB) authentication.

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
    raw_api_key = _get_supplied_api_key(api_key_header, api_key_query)
    token_payload = decode_application_access_token(raw_api_key)

    service_details = await ApplicationV2.find_one(
        ApplicationV2.id == token_payload.get("id"),
        ApplicationV2.deleted_at == None
    )
    if service_details and service_details.api_key and verify_password_v2(
            raw_api_key, service_details.api_key):
        return raw_api_key

    logger.warning("Invalid Mongo API key for application id %s",
                   token_payload.get("id"))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
