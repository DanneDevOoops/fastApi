#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Application schema for the database
"""

import json
from collections import namedtuple
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from src.db.schemas.schema_config import standard_model_config
from src.utils.nano_id import generate_nano_id


class ApplicationCreate(BaseModel):
    """
    Schema for creating a new Application instance.

    The API key is generated server-side and should not be supplied by the
    client.
    """
    id: Optional[str] = Field(default_factory=generate_nano_id)
    name: str
    description: str
    url: str
    is_active: bool = True

    model_config = standard_model_config


class ApplicationUpdate(BaseModel):
    """
    Schema for updating an existing Application instance.
    
    Note: api_key and timestamps cannot be updated via PATCH.
    Timestamps are automatically managed by the application.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = standard_model_config


class ApplicationOutput(BaseModel):
    """
    Schema for returning an Application instance.
    """
    id: str
    name: str
    description: str
    url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    jwt_token: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at', 'updated_at', 'deleted_at')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[float]:
        """ Serialize datetime to timestamp """
        return value.timestamp() if value else None

    def __str__(self) -> str:
        """
        String representation of the ApplicationOutput instance.

        :return: Object representation as a string
        :rtype: str
        """
        return json.dumps(self.model_dump(), indent=2)

    def __eq__(self, other: object) -> bool:
        """
        Equality comparison between two ApplicationOutput instances.

        :param other: ApplicationOutput instance
        :type other: object
        :return: Boolean value indicating equality
        :rtype: bool
        """
        if isinstance(other, ApplicationOutput):
            return self.model_dump() == other.model_dump()
        return False

    def __ne__(self, other: object) -> bool:
        """
        Inequality comparison between two ApplicationOutput instances.

        :param other: ApplicationOutput instance
        :type other: object
        :return: Boolean value indicating inequality
        :rtype: bool
        """
        return not self.__eq__(other)

    def __getattr__(self, item):
        """
        Returns the value of the attribute with the given name.
        """
        if item in self.model_fields_set:
            return getattr(self, item)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{item}'")

    def as_named_tuple(self) -> tuple:
        """
        Returns the ApplicationOutput instance as a named tuple.

        :return: ApplicationOutput instance as a named tuple
        :rtype: tuple
        """
        return namedtuple(
            'Application',
            self.model_dump().keys())(*self.model_dump().values())
