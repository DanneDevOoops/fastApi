#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Serialization utilities for API v2 database schemas.

This module provides functions to serialize individual and batch database
records, including users and generic items, into dictionary formats
suitable for API responses. It supports both single-object and list
serialization, handling conversion of MongoDB ObjectIds and model instances
to standard Python dictionaries.

Functions:
- individual_serializer: Serialize a single generic database record.
- list_serial: Serialize a list of generic database records.
- user_serializer: Serialize a single User document or model.
- user_list_serializer: Serialize a list of User documents or models.
"""


def individual_serializer(individual):
    """
    Serialize a single generic database record.

    Converts an individual database record (typically a MongoDB document)
    into a dictionary with stringified `id` and selected fields.

    :param individual: The database record to serialize.
    :type individual: dict
    :return: A dictionary representation of the record.
    :rtype: dict
    """
    return {
        "id": str(individual["_id"]),
        "name": individual["name"],
        "description": individual["description"],
        "complete": individual["complete"],
        "api_key": individual["api_key"],
    }


def list_serial(individual):
    """
    Serialize a list of generic database records.

    Applies `individual_serializer` to each record in the provided list.

    :param individual: A list of database records to serialize.
    :type individual: list[dict]
    :return: A list of serialized record dictionaries.
    :rtype: list[dict]
    """
    return list(map(individual_serializer, individual))


def model_serialize(input_data_model) -> dict:
    """
    Serialize a single User document or model.

    Converts a data model instance or dictionary to a standard dictionary,
    stringify the `id` field and removing the MongoDB `_id` key.

    :param input_data_model: The beanie Document model to serialize.
    :type input_data_model: Any
    :return: A dictionary representation of the User.
    :rtype: dict
    """
    data = (
        input_data_model.model_dump()
        if hasattr(input_data_model, "model_dump")
        else (dict(input_data_model))
    )
    if "_id" in data and data["_id"] is not None:
        data["id"] = str(data["_id"])
        del data["_id"]
    return data


def user_list_serializer(users):
    """
    Serialize a list of User documents or models.

    Applies `user_serializer` to each User in the provided list.

    :param users: A list of User documents or models to serialize.
    :type users: list
    :return: A list of serialized User dictionaries.
    :rtype: list[dict]
    """
    return list(map(model_serialize, users))
