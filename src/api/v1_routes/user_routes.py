#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Defines the User API routes for the FastAPI application (v1 – PostgreSQL).

Includes endpoints for creating users, retrieving single or multiple users
(active and soft-deleted), updating user data (PUT & PATCH), soft deleting
users, and permanently deleting users from the PostgreSQL database.
"""

import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.core.custom_exceptions import NotFoundException
from src.core.env_config import get_settings
from src.db.connectors.postgres_db import get_pg_db
from src.db.models.v1_models.users_model_v1 import User
from src.db.schemas.v1_schemas.user_schemas import UserCreate, UserOutput, \
    UserUpdate

# Initialize the API router
router = APIRouter()

# Initialize environment settings & logger
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")

# --- Authentication --------
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.options("", operation_id="options_v1_user_routes")
def options_user_routes() -> Response:
    """
    Handle HTTP OPTIONS requests for the /users endpoint.

    :return: Empty response with status code 204 and Allow header.
    :rtype: Response
    """
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"Allow": "GET, POST, PUT, PATCH, DELETE"},
    )


# ---------------------------------------------------------------------------
# GET /users  –  all active users
# ---------------------------------------------------------------------------
@router.get(
    "",
    name="get_all_users_v1",
    description="Get all active Users from the PostgreSQL database",
    operation_id="get_all_users_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Retrieve all Users that are not soft-deleted.

    :return: A list of active user data.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching all active users from the PostgreSQL database")
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(User.deleted_at.is_(None))
            )
            users = result.unique().scalars().all()

        if not users:
            raise NotFoundException(message="No users found")

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=[UserOutput.model_validate(u).model_dump() for u in users],
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# GET /users/deleted  –  all soft-deleted users
# ---------------------------------------------------------------------------
@router.get(
    "/deleted",
    name="get_all_soft_deleted_users_v1",
    description="Get all soft-deleted Users from the PostgreSQL database",
    operation_id="get_all_soft_deleted_users_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_soft_deleted_users(
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Retrieve all Users that have been soft-deleted.

    :return: A list of soft-deleted user data.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching all soft-deleted users from the PostgreSQL database")
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(User.deleted_at.isnot(None))
            )
            users = result.unique().scalars().all()

        if not users:
            raise NotFoundException(message="No soft-deleted users found")

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=[UserOutput.model_validate(u).model_dump() for u in users],
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# GET /users/activated  –  all active-status users (excluding soft-deleted)
# ---------------------------------------------------------------------------
@router.get(
    "/activated",
    name="get_all_activated_users_v1",
    description="Get all activated Users from the PostgreSQL database",
    operation_id="get_all_activated_users_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_activated_users(
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Retrieve all users where `is_active` is True and not soft-deleted.

    :return: A list of activated user data.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching all activated users from the PostgreSQL database")
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(
                    User.is_active.is_(True),
                    User.deleted_at.is_(None)
                )
            )
            users = result.unique().scalars().all()

        if not users:
            raise NotFoundException(message="No activated users found")

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=[UserOutput.model_validate(u).model_dump() for u in users],
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# GET /users/deactivated  –  all deactivated users (excluding soft-deleted)
# ---------------------------------------------------------------------------
@router.get(
    "/deactivated",
    name="get_all_deactivated_users_v1",
    description="Get all deactivated Users from the PostgreSQL database",
    operation_id="get_all_deactivated_users_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_deactivated_users(
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Retrieve all users where `is_active` is False and not soft-deleted.

    :return: A list of deactivated user data.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching all deactivated users from the PostgreSQL database")
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(
                    User.is_active.is_(False),
                    User.deleted_at.is_(None)
                )
            )
            users = result.unique().scalars().all()

        if not users:
            raise NotFoundException(message="No deactivated users found")

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=[UserOutput.model_validate(u).model_dump() for u in users],
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# GET /users/superusers  –  all superusers (excluding soft-deleted)
# ---------------------------------------------------------------------------
@router.get(
    "/superusers",
    name="get_all_superusers_v1",
    description="Get all superusers from the PostgreSQL database",
    operation_id="get_all_superusers_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_superusers(
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Retrieve all users where `is_superuser` is True and not soft-deleted.

    :return: A list of superuser data.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching all superusers from the PostgreSQL database")
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(
                    User.is_superuser.is_(True),
                    User.deleted_at.is_(None)
                )
            )
            users = result.unique().scalars().all()

        if not users:
            raise NotFoundException(message="No superusers found")

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=[UserOutput.model_validate(u).model_dump() for u in users],
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# GET /users/{user_id}  –  single active user
# ---------------------------------------------------------------------------
@router.get(
    "/{user_id}",
    name="get_user_by_id_v1",
    description="Get a User by ID from the PostgreSQL database",
    operation_id="get_user_by_id_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
        user_id: str,
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Retrieve a single active User by ID.

    :param user_id: The unique identifier of the user.
    :type user_id: str
    :return: The user data if found, or 404 if not found.
    :rtype: ORJSONResponse
    """
    logger.info("Fetching user with ID: %s", user_id)
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(
                    User.id == user_id, User.deleted_at.is_(None)
                )
            )
            user = result.unique().scalar_one_or_none()

        if not user:
            raise NotFoundException(message="User not found")

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=UserOutput.model_validate(user).model_dump(),
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# POST /users  –  create user
# ---------------------------------------------------------------------------
@router.post(
    "",
    name="create_user_v1_in_pg_db",
    description="Create a new User in the PostgreSQL database",
    operation_id="create_user_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Create a new User with a hashed password.

    :param user: The data required to create a new user.
    :type user: UserCreate
    :return: The created user data (excluding sensitive fields), or an error response.
    :rtype: ORJSONResponse
    """
    logger.info("Creating a new user: %s", user.username)
    try:
        new_user = User(**user.model_dump())
        new_user.password = bcrypt_context.hash(new_user.password)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        serialized = UserOutput.model_validate(new_user).model_dump()
        for key in ["password", "is_superuser", "updated_at", "deleted_at"]:
            serialized.pop(key, None)

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=serialized,
        )
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with given details already exists",
        ) from e
    except Exception as e:
        await db.rollback()
        logger.error("Unexpected error creating user: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# POST /users/batch  –  get a batch of users by IDs
# ---------------------------------------------------------------------------
@router.post(
    "/batch",
    name="get_a_batch_of_users_by_ids_v1",
    description="Get a batch of Users by a list of IDs from the PostgreSQL database",
    operation_id="get_a_batch_of_users_by_ids_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_users_batch_by_ids(
        user_ids: List[str],
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Retrieve a batch of active Users by a list of IDs.

    :param user_ids: A list of user IDs to retrieve.
    :type user_ids: List[str]
    :return: A list of user data matching the given IDs.
    :rtype: ORJSONResponse
    """
    logger.info("Requesting users from IDs: %s", user_ids)
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(
                    User.id.in_(user_ids), User.deleted_at.is_(None)
                )
            )
            users = result.unique().scalars().all()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=[UserOutput.model_validate(u).model_dump() for u in users],
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# PATCH /users/delete/{user_id}  –  soft delete
# NOTE: declared before PATCH /{user_id} so "delete" is not treated as user_id
# ---------------------------------------------------------------------------
@router.patch(
    "/delete/{user_id}",
    name="soft_delete_user_by_id_v1",
    description="Soft-delete a User by ID in the PostgreSQL database",
    operation_id="soft_delete_user_by_id_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_delete_user_by_id(
        user_id: str,
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Soft-delete an active User by setting the `deleted_at` timestamp.

    :param user_id: The unique identifier of the user to soft-delete.
    :type user_id: str
    :return: The updated user data, or 404 if not found / already deleted.
    :rtype: ORJSONResponse
    """
    logger.info("Soft-deleting user with ID: %s", user_id)
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(
                    User.id == user_id, User.deleted_at.is_(None)
                )
            )
            user = result.unique().scalar_one_or_none()

            if not user:
                raise NotFoundException(
                    message="User not found or already marked as deleted"
                )

            user.updated_at = datetime.utcnow()
            user.deleted_at = datetime.utcnow()
            await session.commit()
            await session.refresh(user)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=UserOutput.model_validate(user).model_dump(),
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# PATCH /users/{user_id}  –  partial update
# ---------------------------------------------------------------------------
@router.patch(
    "/{user_id}",
    name="patch_update_user_by_id_v1",
    description="Partially update a User's data in the PostgreSQL database",
    operation_id="patch_update_user_by_id_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def patch_update_user_by_id(
        user_id: str,
        user_data: UserUpdate,
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Partially update an active User's data by ID (only provided fields are changed).

    :param user_id: The unique identifier of the user to update.
    :type user_id: str
    :param user_data: The fields and values to update.
    :type user_data: UserUpdate
    :return: The updated user data, or 404 if not found.
    :rtype: ORJSONResponse
    """
    logger.info("PATCH updating user with ID: %s", user_id)
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(
                    User.id == user_id, User.deleted_at.is_(None)
                )
            )
            user = result.unique().scalar_one_or_none()

            if not user:
                raise NotFoundException(message="User not found")

            for field, value in user_data.model_dump(
                    exclude_unset=True).items():
                setattr(user, field, value)
            user.updated_at = datetime.utcnow()
            await session.commit()
            await session.refresh(user)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=UserOutput.model_validate(user).model_dump(),
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# PUT /users/{user_id}  –  full update
# ---------------------------------------------------------------------------
@router.put(
    "/{user_id}",
    name="put_update_user_by_id_v1",
    description="Fully update a User's data in the PostgreSQL database",
    operation_id="put_update_user_by_id_v1_in_pg_db",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def put_update_user_by_id(
        user_id: str,
        user_data: UserUpdate,
        db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Fully replace an active User's data by ID.

    :param user_id: The unique identifier of the user to update.
    :type user_id: str
    :param user_data: The new user data.
    :type user_data: UserUpdate
    :return: The updated user data, or 404 if not found.
    :rtype: ORJSONResponse
    """
    logger.info("PUT updating user with ID: %s", user_id)
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(
                    User.id == user_id, User.deleted_at.is_(None)
                )
            )
            user = result.unique().scalar_one_or_none()

            if not user:
                raise NotFoundException(message="User not found")

            for field, value in user_data.model_dump(
                    exclude_unset=True).items():
                setattr(user, field, value)
            user.updated_at = datetime.utcnow()
            await session.commit()
            await session.refresh(user)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=UserOutput.model_validate(user).model_dump(),
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


# ---------------------------------------------------------------------------
# DELETE /users/delete/{user_id}  –  permanent hard delete
# ---------------------------------------------------------------------------
@router.delete(
    "/delete/{user_id}",
    name="delete_user_by_id_v1",
    description="Permanently delete a User by ID from the PostgreSQL database",
    operation_id="delete_user_by_id_v1_in_pg_db",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_user_by_id(
        user_id: str,
        db: AsyncSession = Depends(get_pg_db),
) -> Response:
    """
    Permanently delete a User by ID.

    :param user_id: The unique identifier of the user to delete.
    :type user_id: str
    :return: Empty 204 response if successful, or 404 if not found.
    :rtype: Response
    """
    logger.info("Permanently deleting user with ID: %s", user_id)
    try:
        async with db as session:
            result = await session.execute(
                select(User).filter(User.id == user_id)
            )
            user = result.unique().scalar_one_or_none()

            if not user:
                raise NotFoundException(message="User not found")

            await session.delete(user)
            await session.commit()

        logger.info("User with ID: %s permanently deleted", user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
