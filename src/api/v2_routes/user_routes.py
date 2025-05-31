#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=singleton-comparison

"""
Implements FastAPI routes for user management in API v2.

Includes endpoints for creating users, retrieving single or multiple users
(active and soft deleted), updating user data, soft deleting users,
and permanently deleting users from the MongoDB database. Each route
handles appropriate request validation, response formatting, and logging.
"""

import logging
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from starlette.responses import Response

from src.core.env_config import get_settings
from src.db.models.v2_models.user_model import CreateUser, User, UsersBatch, \
    PatchUserData
from src.db.serializers.v2_serializers.v2_user_serializers import \
    user_serializer

router = APIRouter()

settings = get_settings()
logger = logging.getLogger(
    settings.app_logger_name or "application_logger")


@router.options("", operation_id="options_user_route_v2")
def options_user_route_v2() -> Response:
    """
    Handle HTTP OPTIONS requests for the user routes in version 2 of the API.

    Returns the allowed HTTP methods for the user resource.

    :return: Empty response with status code 204 and Allow header.
    :rtype: Response
    """
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"Allow": "GET, POST, PUT, PATCH, DELETE"}
    )


@router.get("",
            name="get_all_users_v2",
            description="Get all Users from the MongoDB",
            operation_id="get_all_users_v2",
            response_model=User,
            status_code=status.HTTP_200_OK)
async def get_all_users_v2() -> ORJSONResponse:
    """
    Retrieve all Users in version 2 of the API.

    Returns a list of users who have not been soft deleted (where
    `deleted_at` is None).

    :return: A list of active user data.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching all users from the database")
    all_users = await User.find(User.deleted_at == None).to_list()
    return ORJSONResponse(
        content=list(map(user_serializer, all_users)),
        status_code=status.HTTP_200_OK
    )


@router.get("/deleted",
            name="get_all_soft_deleted_users_v2",
            description="Get all soft deleted Users from the MongoDB",
            operation_id="get_all_soft_deleted_users_v2",
            response_model=User,
            status_code=status.HTTP_200_OK)
async def get_all_soft_deleted_users_v2() -> ORJSONResponse:
    """
    Retrieve all soft deleted Users in version 2 of the API.

    Returns a list of users who have been marked as deleted (where
    `deleted_at` is not None).

    :return: A list of soft deleted user data.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching all soft deleted users from the MongoDB database")
    all_soft_deleted_users = await User.find(
        User.deleted_at != None).to_list()
    return ORJSONResponse(
        content=list(map(user_serializer, all_soft_deleted_users)),
        status_code=status.HTTP_200_OK
    )


@router.get("/{user_id}",
            name="get_user_by_id_v2",
            description="Get a User by ID from the MongoDB",
            operation_id="get_user_by_id_v2",
            response_model=User,
            status_code=status.HTTP_200_OK)
async def get_user_by_id_v2(user_id: str) -> ORJSONResponse:
    """
    Retrieve a User by ID in version 2 of the API.

    Returns the user data if the user exists and is not soft deleted.

    :param user_id: The unique identifier of the user to retrieve.
    :type user_id: str
    :return: The user data if found, or a 404 error if the user does
        not exist.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching user with ID: %s", user_id)
    user = await User.find_one(
        User.id == user_id,
        User.deleted_at == None
    )

    if not user:
        return ORJSONResponse(
            content={"detail": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    return ORJSONResponse(
        content=user_serializer(user),
        status_code=status.HTTP_200_OK
    )


@router.post("",
             name="create_new_user_v2",
             description="Create a new User in the MongoDB",
             operation_id="create_new_user_v2",
             status_code=status.HTTP_201_CREATED,
             response_model=User)
async def create_new_user_v2(user_data: CreateUser) -> ORJSONResponse:
    """
    Create a new User in version 2 of the API.

    Accepts user data in the request body and creates a new user record in
    the database.

    :param user_data: The data required to create a new user.
    :type user_data: CreateUser
    :return: The newly created user data with status code 201.
    :rtype: ORJSONResponse
    """
    new_user = User(**user_data.model_dump())
    logger.info("Creating a new user with data: %s", new_user)
    new_user_in_db = await new_user.create()

    # Placeholder for user creation logic
    return ORJSONResponse(
        content=user_serializer(new_user_in_db),
        status_code=status.HTTP_201_CREATED
    )


@router.post("/batch",
             name="get_a_batch_of_users_by_ids_v2",
             description="Get a batch of Users by a list of IDs",
             operation_id="get_a_batch_of_users_by_ids_v2",
             status_code=status.HTTP_201_CREATED,
             response_model=List[User])
async def get_users_batch_by_ids_v2(
        list_of_user_ids: UsersBatch) -> ORJSONResponse:
    """
    Retrieve a batch of Users by a list of IDs in version 2 of the API.

    Returns user records that match the provided list of IDs and are not
    soft deleted.

    :param list_of_user_ids: The list of user IDs to retrieve.
    :type list_of_user_ids: UsersBatch
    :return: A list of user data matching the given IDs, or an empty list
        if none found.
    :rtype: ORJSONResponse
    """
    logger.info("Requesting users from IDs: %s", list_of_user_ids.id)
    # list_of_users = await User.find_many(list_of_user_ids).to_list()
    list_of_users = await User.find(
        {User.id: {"$in": list_of_user_ids.id},
         User.deleted_at: None}).to_list()

    return ORJSONResponse(
        content=list(map(user_serializer, list_of_users)),
        status_code=status.HTTP_200_OK
    )


@router.post("/delete/{user_id}",
             name="delete_user_by_id_v2",
             description="Delete a User by ID from the MongoDB",
             operation_id="delete_user_by_id_v2",
             status_code=status.HTTP_200_OK,
             response_model=None)
async def soft_delete_user_by_id_v2(user_id: str) -> ORJSONResponse:
    """
    Soft delete a User by ID in version 2 of the API.

    Marks the user as deleted by setting the `deleted_at` field, without
    removing the record from the database.

    :param user_id: The unique identifier of the user to soft delete.
    :type user_id: str
    :return: The user data after being marked as deleted, or a 404 error if
        the user is not found or already deleted.
    :rtype: ORJSONResponse
    """
    logger.info("Soft deleting user with ID: %s", user_id)
    user = await User.find_one(
        User.id == user_id,
        User.deleted_at == None
    )
    if not user:
        return ORJSONResponse(
            content={"detail": "User not found or already marked as deleted"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    user.deleted_at = datetime.now(timezone.utc)
    await user.save()
    return ORJSONResponse(
        content=user_serializer(user),
        status_code=status.HTTP_200_OK
    )


@router.patch("/{user_id}",
              name="patch_update_user_by_id_v2",
              description="Patch update a Users data in the MongoDB",
              operation_id="patch_update_user_by_id_v2",
              status_code=status.HTTP_200_OK,
              response_model=User)
async def patch_update_user_by_id_v2(user_id: str, request_model:
PatchUserData) -> ORJSONResponse:
    """
    Patch update a User's data by ID in version 2 of the API.

    Updates only the fields provided in the request body, leaving other 
    fields unchanged.

    :param user_id: The unique identifier of the user to update.
    :type user_id: str
    :param request_model: The fields and values to update for the user.
    :type request_model: PatchUserData
    :return: The updated user data if successful, or a 404 error if the 
        user is not found.
    :rtype: ORJSONResponse
    """
    logger.info("Updating user with ID: %s", user_id)
    user = await User.find_one(
        User.id == user_id,
        User.deleted_at == None
    )

    if not user:
        return ORJSONResponse(
            content={"detail": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Update user fields with request model data
    for field, value in request_model.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    user.updated_at = datetime.now(timezone.utc)
    updated_user = await user.save()

    return ORJSONResponse(
        content=user_serializer(updated_user),
        status_code=status.HTTP_200_OK
    )


@router.delete("/{user_id}",
               name="delete_user_by_id_v2",
               description="Delete a User by ID from the MongoDB",
               operation_id="delete_user_by_id_v2",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None)
async def delete_user_by_id_v2(user_id: str) -> Response:
    """
    Permanently delete a User by ID from version 2 of the API.

    :param user_id: The unique identifier of the user to delete.
    :type user_id: str
    :return: Empty response with status code 204 if successful, or 404 if
        user not found.
    :rtype: Response
    """
    logger.info("Permanently deleting user with ID: %s", user_id)
    user = await User.find_one(
        User.id == user_id
    )

    if not user:
        return ORJSONResponse(
            content={"detail": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    await user.delete()
    logger.info("User with ID: %s has been permanently deleted", user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
