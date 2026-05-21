#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
User schema for the database
"""

import json
from collections import namedtuple
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.db.schemas.schema_config import standard_model_config
from src.utils.nano_id import generate_nano_id


class UserCreate(BaseModel):
    """
    Schema for creating a new User instance.
    """
    id: Optional[str] = Field(default_factory=generate_nano_id)
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    address: str
    city: str
    state: str
    country: str
    zip_code: str

    # User roles
    is_active: bool = True
    is_superuser: bool = False

    # Timestamps
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()
    deleted_at: Optional[datetime] = None

    @field_serializer('created_at', 'updated_at', 'deleted_at')
    def serialize_datetime(self, value: Optional[datetime]) -> \
            Optional[datetime]:
        """ Serialize datetime to UTC datetime """
        return value if value else None

    model_config = standard_model_config


class UserUpdate(BaseModel):
    """
    Schema for updating an existing User instance.
    """
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None

    # User roles
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    # Timestamps
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @field_serializer('updated_at', 'deleted_at')
    def serialize_datetime(self, value: Optional[datetime]) -> \
            Optional[datetime]:
        """ Serialize datetime to UTC datetime """
        return value if value else None


class UserSimple(BaseModel):
    """
    Schema for retrieving a simple representation of a User instance.
    """
    id: str
    username: str
    email: str
    first_name: str
    last_name: str

    model_config = standard_model_config


class UserOutput(UserCreate):
    """
    Schema for retrieving a User instance.
    """
    id: str
    username: str
    email: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]

    # User roles
    is_active: Optional[bool]
    is_superuser: Optional[bool]

    # Timestamps
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None

    def __str__(self) -> str:
        """
        Returns a string representation of the UserOutput instance.
        """
        return json.dumps(self.dict(), indent=2)

    def __eq__(self, other) -> bool:
        """
        Compares two UserOutput instances for equality.
        """
        return self.dict() == other.dict()

    def __ne__(self, other) -> bool:
        """
        Compares two UserOutput instances for inequality.
        """
        return self.dict() != other.dict()

    def __getattr__(self, item):
        """
        Returns the value of the attribute with the given name.
        """
        if item in self.model_fields_set:
            return getattr(self, item)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{item}'")

    def as_named_tuple(self) -> namedtuple:
        """
        Returns a namedtuple representation of the UserOutput instance.
        """
        user_named_tuple = namedtuple('User', self.model_fields.keys())
        return user_named_tuple(**self.model_dump())
