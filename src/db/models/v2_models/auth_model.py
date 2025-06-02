#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Auth model description here...
"""

from pydantic import BaseModel, field_serializer

from src.db.models.v2_models.user_model import User
from src.db.serializers.v2_serializers.v2_model_serializers import \
    model_serialize


class AuthTokenResponse(BaseModel):
    """
    Model for the authentication token response.
    """
    token: str
    token_type: str
    user: User
    expires_in: int

    @field_serializer('user')
    def remove_sensitive_user_data(self, user: User) -> User:
        """
        Serialize the user object to a dictionary and remove sensitive data.

        :param user: The User object to serialize.
        :return: The User object with sensitive data removed.
        :rtype: User
        """
        model_serialize(user).pop('password', None)
        return user


class UserPasswordSignin(BaseModel):
    """
    Model for user password sign-in.
    """
    email: str
    username: str
    password: str
