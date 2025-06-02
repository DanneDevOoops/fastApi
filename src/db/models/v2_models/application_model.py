#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Application / Services model description here...
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
    Model for the Application document in the database.
    """
    # Unique identifiers
    id: str = Field(alias="_id", default_factory=generate_nano_id)
    index: Indexed(int, pymongo.ASCENDING, unique=True,
                   name="app-index") = Field(default_factory=int)
    name: Indexed(str, pymongo.DESCENDING, unique=True, name="app-name")

    # Details
    description: str = Field(default="No description provided")
    api_key: Optional[str] = None
    ip_adress: str = "http://localhost"
    port: int = 3000

    # Metadata
    tags: Optional[Dict] = Field(default_factory=dict)

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

    # Model configuration
    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """ Settings for the Application model."""
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
    Model for the Application document in the database.
    """
    # Unique identifiers
    id: str = Field(alias="_id")
    index: int
    name: str

    # Details
    description: str
    api_key: str
    token_exposed: str
    ip_adress: str
    port: int

    # Metadata
    tags: Dict

    # Timestamps
    created_at: datetime

    # Model configuration
    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """ Settings for the Application model."""
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
    Model for creating a new application/service.
    """
    # Unique identifiers
    index: Optional[int] = Field(default_factory=int, unique=True)
    name: str

    # Details
    description: Optional[str] = Field(default="No description provided...")
    ip_adress: str = "127.0.0.1"
    port: int = 3000

    # Metadata
    tags: Optional[Dict] = Field(default_factory=dict)

    # Timestamps
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[None | datetime] = None

    # Model configuration
    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """ Settings for the Application model."""
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
    Model for patching an existing application/service.
    """
    # Unique identifiers
    name: Optional[str] = None

    # Details
    description: Optional[str] = None
    ip_adress: Optional[str] = None
    port: Optional[int] = None

    # Metadata
    tags: Optional[Dict] = None

    # Model configuration
    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the PatchUpdateApplication model.
        """
        name = "applications"

        def __str__(self) -> str:
            """
            String representation of the PatchUpdateApplication model.

            :return: The name of the application.
            :rtype: str
            """
            return self.name

        def __dir__(self):
            """
            Return the list of attributes for the PatchUpdateApplication model.

            :return: List of attributes.
            :rtype: list
            """
            return ["name", "description", "ip_adress", "port", "tags"]
