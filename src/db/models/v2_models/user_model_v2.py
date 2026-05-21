#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
User model definitions for MongoDB with Beanie ODM.

This module defines Pydantic and Beanie models for user data, supporting
CRUD operations, batch processing, and schema validation for API v2.
It includes models for user creation, updates (full and partial), and
batch operations, with automatic timestamping and MongoDB ObjectId handling.

Classes:
- User: Main Beanie document model for users.
- UsersBatch: Model for batch user operations.
- CreateUser: Schema for creating a new user.
- PatchUserData: Schema for partial user updates.
- UpdateUser: Schema for full user updates.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

import pymongo
from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, Field

from src.utils.nano_id import generate_nano_id


class UserRole(str, Enum):
    """
    Enum for user roles in the system. Privileges and access levels are
    determined by the role assigned to the user.

    Available roles:
    - USER: Regular user with standard access.
    - ADMIN: User with administrative privileges.
    - SUPERUSER: User with elevated privileges, typically for system
        maintenance or higher level management tasks. This role is the only one
        that can create, update into, or delete admin users.
    """
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"


class User(Document):
    """
    User document model for MongoDB.

    :param id: Unique identifier for the user (MongoDB `_id`).
    :type id: str
    :param username: Username for authentication (unique, indexed).
    :type username: str
    :param index: Unique integer index for the user (indexed).
    :type index: int
    :param role: User role (default: "user").
    :type role: str
    :param password: User password (hashed).
    :type password: str
    :param firstname: User's first name.
    :type firstname: str
    :param lastname: User's last name.
    :type lastname: str
    :param address: User's address.
    :type address: str
    :param zip_code: Postal code.
    :type zip_code: str
    :param city: City of residence.
    :type city: str
    :param country: Country of residence.
    :type country: str
    :param phone: Contact phone number.
    :type phone: str
    :param email: Email address (unique, indexed).
    :type email: str
    :param tags: Additional metadata as key-value pairs.
    :type tags: Optional[Dict]
    :param created_at: Timestamp when the user was created (UTC).
    :type created_at: datetime
    :param updated_at: Timestamp when the user was last updated (UTC).
    :type updated_at: datetime
    :param deleted_at: Timestamp when the user was deleted, if applicable.
    :type deleted_at: Optional[datetime]

    :cvar model_config: Allows arbitrary types and encodes ObjectId as string.
    :cvar Settings: Contains collection name and utility methods.
    """
    id: str = Field(alias="_id", default_factory=generate_nano_id)
    username: Indexed(str, pymongo.TEXT, unique=True, name="user-username")
    index: Indexed(int, pymongo.ASCENDING, unique=True, name="user-index")

    password: str
    role: Indexed(str, unique=False, name="user-role") = Field(
        default=UserRole.USER)

    firstname: str
    lastname: str
    address: str
    zip_code: str
    city: str
    country: str
    phone: str
    email: Indexed(str, pymongo.ASCENDING, unique=True, name="user-email")

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
        Settings for the User model.

        :cvar name: The name of the MongoDB collection for users.
        :type name: str

        :return: String representation of the Settings instance.
        :rtype: str

        :return: List of attributes and methods of the Settings instance.
        :rtype: list
        """
        name = "users"

        def __str__(self) -> str:
            """
            String representation of the Settings instance.
            """
            return f"User.Settings.name: {self.name}"

        def __dir__(self):
            """
            Returns the list of attributes and methods of the Settings
            instance.
            """
            return self.__dict__.keys()


class UsersBatch(BaseModel):
    """
    Represents a batch of user IDs for bulk operations such as deletion,
    updates, or retrieval.

    :param id: List of user IDs included in the batch operation.
    :type id: List[str]

    :cvar Settings: Contains collectio name and utility methods for
        batch operations.
    """
    id: List[str]

    class Settings:
        """
        Settings for the UsersBatch model.

        :cvar name: The name of the MongoDB collection for users.
        :type name: str

        :return: String representation of the Settings instance.
        :rtype: str

        :return: List of attributes and methods of the Settings instance.
        :rtype: list
        """
        name = "users"

        def __str__(self) -> str:
            """
            String representation of the Settings instance.
            """
            return f"UsersBatch.Settings.name: {self.name}"

        def __dir__(self):
            """
            Returns the list of attributes and methods of the Settings
            instance.
            """
            return self.__dict__.keys()


class CreateUser(BaseModel):
    """
    Represents a request to create a new user.

    :param index: Unique integer index for the user (optional,
        auto-generated).
    :type index: Optional[int]
    :param username: Username for authentication.
    :type username: str
    :param password: User password (hashed).
    :type password: str
    :param firstname: User's first name.
    :type firstname: str
    :param lastname: User's last name.
    :type lastname: str
    :param address: User's address.
    :type address: str
    :param zip_code: Postal code.
    :type zip_code: str
    :param city: City of residence.
    :type city: str
    :param country: Country of residence.
    :type country: str
    :param email: Email address.
    :type email: str
    :param phone: Contact phone number.
    :type phone: str
    :param tags: Additional metadata as key-value pairs.
    :type tags: Optional[Dict]
    :param created_at: Timestamp when the user was created (UTC).
    :type created_at: Optional[datetime]
    :param updated_at: Timestamp when the user was last updated (UTC).
    :type updated_at: Optional[datetime]
    :param deleted_at: Timestamp when the user was deleted, if applicable.
    :type deleted_at: Optional[datetime]

    :cvar model_config: Allows arbitrary types and encodes ObjectId as string.
    :cvar Settings: Contains collection name and utility methods.
    """
    index: Optional[int] = Field(default_factory=int, unique=True)
    username: str
    password: str
    firstname: str
    lastname: str
    address: str
    zip_code: str
    city: str
    country: str
    email: str
    phone: str
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
        Settings for the User model.

        :cvar name: The name of the MongoDB collection for users.
        :type name: str

        :return: String representation of the Settings instance.
        :rtype: str

        :return: List of attributes and methods of the Settings instance.
        :rtype: list
        """
        name = "users"

        def __str__(self) -> str:
            """
            String representation of the Settings instance.
            """
            return f"User.Settings.name: {self.name}"

        def __dir__(self):
            """
            Returns the list of attributes and methods of the Settings
            instance.
            """
            return self.__dict__.keys()


class PatchUserData(CreateUser):
    """
    Represents a request to partially update user information.

    :param firstname: User's first name (optional,
        can be omitted or set to None).
    :type firstname: Optional[str]
    :param lastname: User's last name (optional,
        can be omitted or set to None).
    :type lastname: Optional[str]
    :param address: User's address (optional,
        can be omitted or set to None).
    :type address: Optional[str]
    :param zip_code: Postal code (optional, can be
        omitted, or set to None).
    :type zip_code: Optional[str]
    :param city: City of residence (optional, can be
        omitted, or set to None).
    :type city: Optional[str]
    :param country: Country of residence (optional, can be
        omitted, or set to None).
    :type country: Optional[str]
    :param phone: Contact phone number (optional, can be
        omitted, or set to None).
    :type phone: Optional[str]
    :param email: Email address (optional, can be omitted
        or set to None).
    :type email: Optional[str]
    :param tags: Additional metadata as key-value pairs (optional,
        can be omitted, or set to None).
    :type tags: Optional[Dict]
    """
    username: Optional[str] = None
    password: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tags: Optional[Dict] = None


class PutUserData(BaseModel):
    """
    Represents a request to update a user with full data replacement.

    :param username: Username for authentication (optional).
    :type username: Optional[str]
    :param role: User role (optional).
    :type role: Optional[str]
    :param firstname: User's first name.
    :type firstname: str
    :param lastname: User's last name.
    :type lastname: str
    :param address: User's address.
    :type address: str
    :param zip_code: Postal code.
    :type zip_code: str
    :param city: City of residence.
    :type city: str
    :param country: Country of residence.
    :type country: str
    :param phone: Contact phone number.
    :type phone: str
    :param email: Email address (optional).
    :type email: Optional[str]
    :param tags: Additional metadata as key-value pairs (optional).
    :type tags: Optional[Dict]
    """
    username: Optional[str] = None
    role: Optional[str] = None
    firstname: str
    lastname: str
    address: str
    zip_code: str
    city: str
    country: str
    phone: str
    email: Optional[str] = None
    tags: Optional[Dict] = None

    class Settings:
        """
        Settings for the User model.

        :cvar name: The name of the MongoDB collection for users.
        :type name: str

        :return: String representation of the Settings instance.
        :rtype: str

        :return: List of attributes and methods of the Settings instance.
        :rtype: list
        """
        name = "users"

        model_config = {
            "arbitrary_types_allowed": True,
            "json_encoders": {ObjectId: str}
        }

        def __str__(self) -> str:
            """
            String representation of the Settings instance.
            """
            return f"CreateUser.Settings.name: {self.name}"

        def __dir__(self):
            """
            Returns the list of attributes and methods of the Settings
            instance.
            """
            return self.__dict__.keys()


class DeleteUser(BaseModel):
    """
    Represents a request to delete a user by ID.

    :param id: Unique identifier of the user to be deleted.
    :type id: str

    :cvar model_config: Allows arbitrary types and encodes ObjectId as string.
    :cvar Settings: Contains collection name and utility methods.
    """
    id: str

    class Settings:
        """
        Settings for the User model.

        :cvar name: The name of the MongoDB collection for users.
        :type name: str

        :return: String representation of the Settings instance.
        :rtype: str

        :return: List of attributes and methods of the Settings instance.
        :rtype: list
        """
        name = "users"

        model_config = {
            "arbitrary_types_allowed": True,
            "json_encoders": {ObjectId: str}
        }

        def __str__(self) -> str:
            """
            String representation of the Settings instance.
            """
            return f"CreateUser.Settings.name: {self.name}"

        def __dir__(self):
            """
            Returns the list of attributes and methods of the Settings
            instance.
            """
            return self.__dict__.keys()
