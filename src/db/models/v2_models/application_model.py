#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module provides data models for representing, creating, updating,
and deleting application or service records in a database. It defines
schemas for application documents, including metadata, configuration,
and utility settings, supporting both full and partial updates as well as
deletion operations. The models are designed for integration with MongoDB
and Beanie ODM, ensuring type safety, validation, and consistent structure
for application data management.
"""

from datetime import datetime, timezone
from typing import Optional, Dict

import pymongo
from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, Field

from src.utils.nano_id import generate_nano_id


class Application(Document):
    """
    Represents an application document stored in the database.

    :param id: Unique identifier of the application (MongoDB `_id`).
    :type id: str
    :param index: Unique index for the application.
    :type index: int
    :param name: Name of the application.
    :type name: str
    :param description: Description of the application.
    :type description: str
    :param api_key: API key associated with the application (optional).
    :type api_key: Optional[str]
    :param ip_adress: IP address or URL of the application.
    :type ip_adress: str
    :param port: Port number for the application.
    :type port: int
    :param tags: Additional metadata as key-value pairs (optional).
    :type tags: Optional[Dict]
    :param created_at: Timestamp when the application was created (UTC).
    :type created_at: datetime
    :param updated_at: Timestamp when the application was last updated (UTC).
    :type updated_at: datetime
    :param deleted_at: Timestamp when the application was deleted,
        if applicable.
    :type deleted_at: Optional[datetime]

    :cvar model_config: Allows arbitrary types and encodes
        ObjectId as string.
    :cvar Settings: Contains collection name and utility methods
        for the model.
    """
    id: str = Field(alias="_id", default_factory=generate_nano_id)
    index: Indexed(int, pymongo.ASCENDING, unique=True,
                   name="app-index") = Field(default_factory=int)
    name: Indexed(str, pymongo.DESCENDING, unique=True, name="app-name")

    description: str = Field(default="No description provided")
    api_key: Optional[str] = None
    ip_adress: str = "http://localhost"
    port: int = 3000
    tags: Optional[Dict] = Field(default_factory=dict)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the Application model.

        :cvar name: The name of the MongoDB collection for applications.
        :type name: str

        :return __str__: The name of the application (collection).
        :rtype __str__: str

        :return __dir__: List of attribute names relevant to the
            Application model.
        :rtype __dir__: list
        """
        name = "applications"

        def __str__(self) -> str:
            """
            String representation of the Application model.

            :return: The name of the application.
            :rtype: str
            """
            return self.name

        def __dir__(self):
            """
            Return the list of attributes for the Application model.

            :return: List of attributes.
            :rtype: list
            """
            return ["name", "index", "description", "api_key", "host_ip",
                    "host_port", "tags", "created_at", "updated_at",
                    "deleted_at"]


class NewApplication(BaseModel):
    """
    Represents a new application document in the database.

    :param id: Unique identifier of the application (MongoDB `_id`).
    :type id: str
    :param index: Unique index for the application.
    :type index: int
    :param name: Name of the application.
    :type name: str
    :param description: Description of the application.
    :type description: str
    :param api_key: API key associated with the application.
    :type api_key: str
    :param token_exposed: Exposed token for the application.
    :type token_exposed: str
    :param ip_adress: IP address of the application.
    :type ip_adress: str
    :param port: Port number for the application.
    :type port: int
    :param tags: Additional metadata as key-value pairs.
    :type tags: Dict
    :param created_at: Timestamp when the application was created (UTC).
    :type created_at: datetime

    :cvar model_config: Allows arbitrary types and encodes
        ObjectId as string.
    :cvar Settings: Contains collection name and utility methods
        for the model.
    """
    id: str = Field(alias="_id")
    index: int
    name: str
    description: str
    api_key: str
    token_exposed: str
    ip_adress: str
    port: int
    tags: Dict
    created_at: datetime

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the Application model.

        :cvar name: The name of the MongoDB collection for applications.
        :type name: str

        :return __str__: The name of the application (collection).
        :rtype __str__: str

        :return __dir__: List of attribute names relevant to the
            Application model.
        :rtype __dir__: list
        """
        name = "applications"

        def __str__(self) -> str:
            """
            String representation of the Application model.

            :return: The name of the application.
            :rtype: str
            """
            return self.name

        def __dir__(self):
            """
            Return the list of attributes for the Application model.

            :return: List of attributes.
            :rtype: list
            """
            return ["name", "index", "description", "api_key", "host_ip",
                    "host_port", "tags", "created_at", "updated_at",
                    "deleted_at"]


class CreateApplication(BaseModel):
    """
    Represents a request to create a new application or service.

    :param index: Optional unique index for the application.
    :type index: Optional[int]
    :param name: Name of the application.
    :type name: str
    :param description: Description of the application (optional).
    :type description: Optional[str]
    :param ip_adress: IP address of the application.
    :type ip_adress: str
    :param port: Port number for the application.
    :type port: int
    :param tags: Additional metadata as key-value pairs (optional).
    :type tags: Optional[Dict]
    :param created_at: Timestamp when the application was
        created (UTC, optional).
    :type created_at: Optional[datetime]
    :param updated_at: Timestamp when the application was last
        updated (UTC, optional).
    :type updated_at: Optional[datetime]
    :param deleted_at: Timestamp when the application was deleted,
        if applicable.
    :type deleted_at: Optional[datetime]

    :cvar model_config: Allows arbitrary types and encodes
        ObjectId as string.
    :cvar Settings: Contains collection name and utility methods
        for the model.
    """
    index: Optional[int] = Field(default_factory=int, unique=True)
    name: str
    description: Optional[str] = Field(default="No description provided...")
    ip_adress: str = "127.0.0.1"
    port: int = 3000
    tags: Optional[Dict] = Field(default_factory=dict)

    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[None | datetime] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the Application model.

        :cvar name: The name of the MongoDB collection for applications.
        :type name: str

        :return __str__: The name of the application (collection).
        :rtype __str__: str

        :return __dir__: List of attribute names relevant to the
            Application model.
        :rtype __dir__: list
        """
        name = "applications"

        def __str__(self) -> str:
            """
            String representation of the Application model.

            :return: The name of the application.
            :rtype: str
            """
            return self.name

        def __dir__(self):
            """
            Return the list of attributes for the Application model.

            :return: List of attributes.
            :rtype: list
            """
            return [
                "name", "index", "description", "api_key", "host_ip",
                "host_port", "tags", "created_at", "updated_at",
                "deleted_at"]


class PatchUpdateApplication(BaseModel):
    """
    Represents a request to partially update an existing application or
    service.

    :param name: New name for the application (optional).
    :type name: Optional[str]
    :param description: Updated description of the application (optional).
    :type description: Optional[str]
    :param ip_adress: Updated IP address of the application (optional).
    :type ip_adress: Optional[str]
    :param port: Updated port number for the application (optional).
    :type port: Optional[int]
    :param tags: Additional metadata as key-value pairs (optional).
    :type tags: Optional[Dict]

    :cvar model_config: Allows arbitrary types and encodes
        ObjectId as string.
    :cvar Settings: Contains collection name and utility methods for
        the model.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    ip_adress: Optional[str] = None
    port: Optional[int] = None
    tags: Optional[Dict] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the PatchUpdateApplication model.

        :cvar name: The name of the MongoDB collection for applications.
        :type name: str

        :return: String representation of the Settings instance.
        :rtype: str

        :return: List of attributes for the PatchUpdateApplication model.
        :rtype: list
        """
        name = "applications"

        def __str__(self) -> str:
            """
            String representation of the Application model.

            :return: The name of the application.
            :rtype: str
            """
            return self.name

        def __dir__(self):
            """
            Return the list of attributes for the Application model.

            :return: List of attributes.
            :rtype: list
            """
            return ["name", "description", "ip_adress", "port", "tags"]


class PutApplicationData(BaseModel):
    """
    some...
    """
    name: str
    description: str
    ip_adress: str
    port: int
    tags: Optional[Dict] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the PutApplicationData model.

        :cvar name: The name of the MongoDB collection for applications.
        :type name: str

        :return: String representation of the Settings instance.
        :rtype: str

        :return: List of attributes for the PutApplicationData model.
        :rtype: list
        """
        name = "applications"

        def __str__(self) -> str:
            return self.name

        def __dir__(self):
            return ["name", "description", "ip_adress", "port", "tags"]


class DeleteApplication(BaseModel):
    """
    Represents a request to delete an existing application or service.

    :param id: Unique identifier of the application to be
        deleted (MongoDB `_id`).
    :type id: str

    :cvar model_config: Allows arbitrary types and encodes ObjectId as string.
    :cvar Settings: Contains collection name and utility methods for
        the model.
    """
    id: str = Field(alias="_id")

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the DeleteApplication model.

        :cvar name: The name of the MongoDB collection for applications.
        :type name: str

        :return: String representation of the Settings instance.
        :rtype: str

        :return: List of attributes and methods of the Settings instance.
        :rtype: list
        """
        name = "applications"

        def __str__(self) -> str:
            """
            String representation of the Application model.

            :return: The name of the application.
            :rtype: str
            """
            return self.name

        def __dir__(self):
            """
            Return the list of attributes for the Application model.

            :return: List of attributes.
            :rtype: list
            """
            return ["id"]
