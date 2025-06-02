#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=singleton-comparison


"""
This module contains the authentication logic for the FastAPI application.
"""

import logging
from datetime import datetime, timedelta, timezone

from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyQuery, APIKeyHeader, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.core.env_config import get_settings
from src.db.models.v2_models.application_model import Application

settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")

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


def hash_key_v2(input_password: str) -> str:
    """
    Encrypt the input password using bcrypt hashing.

    :param input_password: The plain text password to encrypt.
    :return: The hashed password.
    :rtype: str
    """
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
    token_expires_delta = datetime.utcnow() + expires_in_delta
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
        username: str = payload.get("sub")
        user_id: str = payload.get("id")

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
    encode_object = {
        "sub": app_name,
        "id": app_id
    }

    if expires_in_sec is not None:
        expires_in_delta = timedelta(minutes=expires_in_sec)
        token_expires_delta = datetime.utcnow() + expires_in_delta
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
    if api_key_header:
        if token_payload := decode_application_access_token(api_key_header):
            # Fetch the service details to verify the API key against
            service_details = await Application.find_one(
                Application.id == token_payload.get("id"),
                Application.deleted_at == None
            )
            if verify_password_v2(api_key_header, service_details.api_key):
                return api_key_header

    elif api_key_query:
        if token_payload := decode_application_access_token(api_key_query):
            # Fetch the service details to verify the API key against
            service_details = await Application.find_one(
                Application.id == token_payload.get("id"),
                Application.deleted_at == None
            )
            if verify_password_v2(api_key_query, service_details.api_key):
                return api_key_query

    # This part only happens if the API key is not found in the allowed
    # keys to trigger the warning log and raise an HTTPException return.
    logger.warning('API key not invalid or found')

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
