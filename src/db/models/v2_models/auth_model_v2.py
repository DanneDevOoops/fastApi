#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module defines data models for authentication and user sign-in processes.
It provides schemas for handling authentication token responses and user
credentials, supporting secure serialization and validation of authentication
data. The models are designed for integration with user management systems,
ensuring type safety and consistent structure for authentication workflows.
"""

from pydantic import BaseModel, field_serializer

from src.db.models.v2_models.user_model_v2 import User
from src.db.serializers.v2_serializers.v2_model_serializers import \
    model_serialize


class AuthTokenResponse(BaseModel):
    """
    Represents the response returned after successful authentication.

    :param token: The authentication token issued to the user.
    :type token: str
    :param token_type: The type of the authentication token.
    :type token_type: str
    :param user: The authenticated user object.
    :type user: User
    :param expires_in: The number of seconds until the token expires.
    :type expires_in: int
    """
    token: str
    token_type: str
    user: User
    expires_in: int

    @field_serializer('user')
    def remove_sensitive_user_data(self, user: User) -> User:
        """
        Serialize the user object and remove sensitive data before returning.

        :param user: The User object to serialize.
        :type user: User
        :return: The User object with sensitive data removed.
        :rtype: User
        """
        model_serialize(user).pop('password', None)
        return user


class UserPasswordSignin(BaseModel):
    """
    Represents the data required for user password sign-in.

    :param email: The user's email address.
    :type email: str
    :param username: The user's username.
    :type username: str
    :param password: The user's password.
    :type password: str
    """
    email: str
    username: str
    password: str
