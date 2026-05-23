#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=singleton-comparison


"""
Auth routes description here...
"""

import logging

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from src.core.auth import create_user_access_token, verify_password_v2
from src.core.env_config import get_settings
from src.db.models.v2_models.auth_model_v2 import UserPasswordSignin
from src.db.models.v2_models.user_model_v2 import User
from src.db.serializers.v2_serializers.v2_model_serializers import \
    model_serialize

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(
    settings.app_logger_name or "application_logger")


@router.post("/signin",
             status_code=status.HTTP_200_OK or status.HTTP_401_UNAUTHORIZED)
async def signin_user(signin_data: UserPasswordSignin) -> ORJSONResponse:
    """
    Sign in a user and return the user data.
    """
    user_data = await User.find_one(
        User.username == signin_data.username,
        User.email == signin_data.email,
        User.deleted_at == None
    )

    if not user_data:
        logger.warning("User not found with credentials username: %s and "
                       "email: %s", signin_data.username, signin_data.email)
        return ORJSONResponse(
            content={"detail": "Unauthorized, invalid user credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # Fail fast if user data is not found or verification is invalid
    if not user_data or not verify_password_v2(
            signin_data.password, user_data.password):
        logger.warning("Unauthorized, invalid user credentials")
        return ORJSONResponse(
            content={"detail": "Unauthorized, invalid user credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # Serialize user data and create access token
    serialized_user_data = model_serialize(user_data)
    user_access_token = create_user_access_token(
        signin_data.username, serialized_user_data['id'],
        serialized_user_data['role'])

    # TODO: Determine which fields should be removed  # pylint: disable=W0511
    #  from the response, if any?  # pylint: disable=W0511
    # pylint: enable=W0511
    # Remove some potentially sensitive data from the user response.
    # The idea is to not show hints, etc. that could be used to exploit the
    # application or the user account.
    # Note: All passwords are hashed and not stored in plain text but we
    # still protect it to the best of our abilities.
    for key in ['password', 'role', 'updated_at', 'deleted_at']:
        serialized_user_data.pop(key, None)

    logging.info(
        "User %s signed in successfully",
        serialized_user_data["id"])

    return ORJSONResponse(
        content={
            'user': serialized_user_data,
            'token': user_access_token,
            'token_type': settings.app_jwt_token_type,
            'expires_in': settings.app_jwt_expiration
        },
        status_code=status.HTTP_200_OK
    )
