#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module contains utility functions for MongoDB interactions.

The utility functions are defined as classes, each representing a specific
type of data used in the application.

The following classes are defined:

- PyObjectId: Custom class for Pydantic to parse ObjectId.

Each class includes a detailed docstring with information about its
purpose, the parameters it takes, the response it returns, and any
exceptions it might raise.
"""

from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Custom class for Pydantic to parse ObjectId.

    This class defines the following methods:

    - __get_validators__: Returns a generator that yields the validate method.
    - validate: Validates the ObjectId.
    - __get_pydantic_json_schema__: Modifies the schema.

    Each method includes a detailed docstring with information about its
    purpose, the parameters it takes, the response it returns, and any
    exceptions it might raise.
    """

    @classmethod
    def __get_validators__(cls):
        """
        Returns a generator that yields the validate method.

        :return: A generator that yields the validate method.
        :rtype: generator

        """
        yield cls.validate

    @classmethod
    def validate(cls, v) -> ObjectId:
        """
        Validates the ObjectId.

        :param v: The value to validate.
        :type v: str
        :return: The validated ObjectId.
        :rtype: ObjectId
        :raises ValueError: If the value is not a valid ObjectId.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        """
        Modifies the schema.

        :param field_schema: The field schema to modify.
        :type field_schema: dict
        """
        field_schema.update(type="string")
