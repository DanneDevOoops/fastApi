#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Defines the Application API routes for the FastAPI v1 application.

This module provides endpoints for managing applications/services registered
in the PostgreSQL database, including creation, retrieval, updating, and
soft/hard deletion of application records.
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import build_application_api_credentials
from src.core.custom_exceptions import (
    ConflictException,
    InternalServerException,
    NotFoundException,
)
from src.core.env_config import get_settings
from src.db.connectors.postgres_db import get_pg_db
from src.db.models.v1_models.applications_model_v1 import Application
from src.db.schemas.v1_schemas.application_schemas import (
    ApplicationCreate,
    ApplicationOutput,
    ApplicationUpdate,
)

# Initialize the API router
router = APIRouter()

# Initialize environment settings & logger
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")


@router.options("", operation_id="options_application_routes_v1")
def application_routes_options() -> Response:
    """
    Handle OPTIONS requests for the application routes.
    This is used to support CORS preflight requests.
    """
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={"Allow": "GET, POST, PUT, PATCH, DELETE"},
    )


@router.get(
    "",
    name="get_all_applications_route_v1",
    description="Route to request all registered applications/"
    "services from the PostgreSQL database.",
    operation_id="get_all_applications_route_v1",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_applications(db: AsyncSession = Depends(get_pg_db)) -> ORJSONResponse:
    """
    Get all registered applications/services that are not soft-deleted.
    """
    try:
        logger.info("Getting all registered applications/services...")
        stmt = select(Application).where(Application.deleted_at.is_(None))
        result = await db.execute(stmt)
        applications = result.scalars().all()

        if not applications:
            raise NotFoundException(message="No applications found")

        return ORJSONResponse(
            content=[
                ApplicationOutput.model_validate(app).model_dump()
                for app in applications
            ],
            status_code=status.HTTP_200_OK,
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error("Unexpected error occurred: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


@router.get(
    "/deleted",
    name="get_all_soft_deleted_applications_route_v1",
    description="Route to request all soft-deleted applications/"
    "services from the PostgreSQL database.",
    operation_id="get_all_deleted_applications_route_v1",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_soft_deleted_applications(
    db: AsyncSession = Depends(get_pg_db),
) -> ORJSONResponse:
    """
    Get all soft-deleted applications/services.
    """
    try:
        logger.info("Getting all soft-deleted applications/services...")
        stmt = select(Application).where(Application.deleted_at.is_not(None))
        result = await db.execute(stmt)
        applications = result.scalars().all()

        if not applications:
            raise NotFoundException(message="No deleted applications found")

        return ORJSONResponse(
            content=[
                ApplicationOutput.model_validate(app).model_dump()
                for app in applications
            ],
            status_code=status.HTTP_200_OK,
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error("Unexpected error occurred: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


@router.get(
    "/{app_id}",
    name="get_application_by_id_route_v1",
    description="Route to request a specific application/service by "
    "its ID from the PostgreSQL database.",
    operation_id="get_application_by_id_route_v1",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_application_by_id(
    app_id: str, db: AsyncSession = Depends(get_pg_db)
) -> ORJSONResponse:
    """
    Get a specific application/service by its ID.

    :param app_id: The ID of the application/service to retrieve.
    :param db: The database session.
    :return: ORJSONResponse containing the application/service data.
    """
    try:
        logger.info("Getting application/service with ID %s", app_id)
        stmt = select(Application).where(
            Application.id == app_id, Application.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        app = result.scalar_one_or_none()

        if not app:
            logger.warning("Application with ID %s not found.", app_id)
            raise NotFoundException(message=f"Application ({app_id}) not found")

        return ORJSONResponse(
            content=ApplicationOutput.model_validate(app).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        logger.error("Unexpected error occurred: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


@router.post(
    "",
    name="create_application_route_v1",
    description="Route to create a new application/service in the "
    "PostgreSQL database.",
    operation_id="create_application_route_v1",
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_application(
    app_data: ApplicationCreate, db: AsyncSession = Depends(get_pg_db)
) -> ORJSONResponse:
    """
    Create a new application/service in PostgreSQL.

    :param app_data: The application/service data to create.
    :param db: The database session.
    :return: ORJSONResponse containing the created application/service data.
    """
    try:
        logger.info("Creating a new application/service...")
        app_identifier = app_data.id or ""

        # Generate JWT token and hash it for the API key
        jwt_token, hashed_api_key = build_application_api_credentials(
            app_name=app_data.name,
            app_id=app_identifier,
        )

        # Create the application record
        new_app = Application(
            id=app_identifier,
            name=app_data.name,
            description=app_data.description,
            url=app_data.url,
            is_active=app_data.is_active,
            api_key=hashed_api_key,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        db.add(new_app)
        await db.commit()
        await db.refresh(new_app)

        # Prepare response with JWT token (only displayed once)
        response_data = ApplicationOutput.model_validate(new_app).model_dump()
        response_data["jwt_token"] = jwt_token

        return ORJSONResponse(
            content=response_data, status_code=status.HTTP_201_CREATED
        )
    except IntegrityError as e:
        await db.rollback()
        logger.error("Application already exists: %s", e)
        raise ConflictException(
            message="Application with given details already exists"
        ) from e
    except Exception as e:
        await db.rollback()
        logger.error("Unexpected error occurred: %s", e, exc_info=True)
        raise InternalServerException(message="Internal Server Error") from e


@router.patch(
    "/{app_id}",
    name="update_application_route_v1",
    description="Route to update an existing application/service in "
    "the PostgreSQL database.",
    operation_id="update_application_route_v1",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def patch_update_application(
    app_id: str, app_data: ApplicationUpdate, db: AsyncSession = Depends(get_pg_db)
) -> ORJSONResponse:
    """
    Partially update an existing application/service.

    :param app_id: The ID of the application to update.
    :param app_data: The fields to update.
    :param db: The database session.
    :return: ORJSONResponse containing the updated application data.
    """
    try:
        logger.info("Updating application/service with ID %s", app_id)
        stmt = select(Application).where(
            Application.id == app_id, Application.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        app = result.scalar_one_or_none()

        if not app:
            logger.warning("Application with ID %s not found.", app_id)
            raise NotFoundException(message=f"Application ({app_id}) not found")

        # Update only provided fields
        update_data = app_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(app, key, value)

        app.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(app)

        return ORJSONResponse(
            content=ApplicationOutput.model_validate(app).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        await db.rollback()
        logger.error("Unexpected error occurred: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


@router.put(
    "/{app_id}",
    name="full_update_application_route_v1",
    description="Route to fully update an existing application/"
    "service in the PostgreSQL database using PUT "
    "method.",
    operation_id="full_update_application_route_v1",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def put_update_application(
    app_id: str, app_data: ApplicationCreate, db: AsyncSession = Depends(get_pg_db)
) -> ORJSONResponse:
    """
    Fully update an existing application/service using PUT method.

    :param app_id: The ID of the application to update.
    :param app_data: The complete application data.
    :param db: The database session.
    :return: ORJSONResponse containing the updated application data.
    """
    try:
        logger.info("Fully updating application/service with ID %s using PUT", app_id)
        stmt = select(Application).where(
            Application.id == app_id, Application.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        app = result.scalar_one_or_none()

        if not app:
            logger.warning("Application with ID %s not found.", app_id)
            raise NotFoundException(message=f"Application ({app_id}) not found")

        # Update all fields from request
        app.name = app_data.name
        app.description = app_data.description
        app.url = app_data.url
        app.is_active = app_data.is_active
        app.updated_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(app)

        return ORJSONResponse(
            content=ApplicationOutput.model_validate(app).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        await db.rollback()
        logger.error("Unexpected error occurred: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


@router.patch(
    "/delete/{app_id}",
    name="soft_delete_application_route_v1",
    description="Route to soft delete an existing application/"
    "service from the PostgreSQL database.",
    operation_id="soft_delete_application_route_v1",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def soft_delete_application(
    app_id: str, db: AsyncSession = Depends(get_pg_db)
) -> ORJSONResponse:
    """
    Soft delete an existing application/service by its ID.

    :param app_id: The ID of the application to delete.
    :param db: The database session.
    :return: ORJSONResponse with deletion confirmation.
    """
    try:
        logger.info("Soft deleting application/service with ID %s", app_id)
        stmt = select(Application).where(
            Application.id == app_id, Application.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        app = result.scalar_one_or_none()

        if not app:
            logger.warning("Application with ID %s not found.", app_id)
            raise NotFoundException(message=f"Application ({app_id}) not found")

        # Soft delete by setting deleted_at timestamp
        app.deleted_at = datetime.now(timezone.utc)
        await db.commit()

        return ORJSONResponse(
            content={"detail": f"Application {app_id} " "soft deleted successfully"},
            status_code=status.HTTP_200_OK,
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        await db.rollback()
        logger.error("Unexpected error occurred: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e


@router.delete(
    "/delete/{app_id}",
    name="hard_delete_application_route_v1",
    description="Route to hard delete an existing application/"
    "service from the PostgreSQL database.",
    operation_id="hard_delete_application_route_v1",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def hard_delete_application(
    app_id: str, db: AsyncSession = Depends(get_pg_db)
) -> ORJSONResponse:
    """
    Hard delete an existing application/service by its ID.

    :param app_id: The ID of the application to delete.
    :param db: The database session.
    :return: ORJSONResponse with deletion confirmation.
    """
    try:
        logger.info("Hard deleting application/service with ID %s", app_id)
        stmt = select(Application).where(Application.id == app_id)
        result = await db.execute(stmt)
        app = result.scalar_one_or_none()

        if not app:
            logger.warning("Application with ID %s not found.", app_id)
            raise NotFoundException(message=f"Application ({app_id}) not found")

        # Hard delete from database
        await db.delete(app)
        await db.commit()

        return ORJSONResponse(
            content={"detail": f"Application {app_id} " "deleted successfully"},
            status_code=status.HTTP_200_OK,
        )
    except NotFoundException as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        await db.rollback()
        logger.error("Unexpected error occurred: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from e
