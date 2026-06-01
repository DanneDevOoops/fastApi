#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=singleton-comparison


"""
Write a good module docstring here...
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, status
from fastapi.responses import Response

from src.core.auth import create_application_access_token, hash_key_v2
from src.core.env_config import get_settings
from src.core.responses import AppJSONResponse
from src.db.models.v2_models.application_model_v2 import (
    Application,
    CreateApplication,
    NewApplication,
    PatchUpdateApplication,
    PutApplicationData,
)
from src.db.serializers.v2_serializers.v2_model_serializers import model_serialize

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")


@router.options("", operation_id="options_application_routes_v2")
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
    name="get_all_applications_route_v2",
    description="Route to request all registered "
    "applications/services from the mongo database.",
    operation_id="get_all_applications_route_v2",
    response_model=Application,
    status_code=status.HTTP_200_OK,
)
async def get_all_applications() -> AppJSONResponse:
    """
    Get all registered applications/services.
    """
    logger.info("Getting all registered applications/services...")
    all_applications = await Application.find(Application.deleted_at == None).to_list()

    return AppJSONResponse(
        content=list(map(model_serialize, all_applications)),
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/{app_id}",
    name="get_application_by_id_route_v2",
    description="Route to request a specific application/service "
    "by its ID from the mongo database.",
    operation_id="get_application_by_id_route_v2",
    response_model=Application,
    status_code=status.HTTP_200_OK,
)
async def get_application_by_id(app_id: str) -> AppJSONResponse:
    """
    Get a specific application/service by its ID.

    :param app_id: The ID of the application/service to retrieve.
    :return: AppJSONResponse containing the application/service data.
    """
    logger.info("Getting application/service with ID %s", app_id)
    app = await Application.find_one(
        Application.id == app_id, Application.deleted_at == None
    )

    if not app:
        logger.warning("Application with ID %s not found.", app_id)
        return AppJSONResponse(
            content={"detail": "Application not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return AppJSONResponse(content=model_serialize(app), status_code=status.HTTP_200_OK)


@router.post(
    "",
    name="create_application_route_v2",
    description="Route to create a new application/service " "in the mongo database.",
    operation_id="create_application_route_v2",
    response_model=NewApplication,
    status_code=status.HTTP_201_CREATED,
)
async def create_application(app_data: CreateApplication) -> AppJSONResponse:
    """
    Create a new application/service.

    :param application: The application/service data to create.
    :return: AppJSONResponse containing the created application/service data.
    """
    logger.info("Creating a new application/service...")
    new_app = Application(**app_data.model_dump(exclude_unset=True))

    # Find the current max index and increment it for the new application
    last_app = await Application.find().sort("-index").first_or_none()
    next_index = (last_app.index + 1) if last_app and last_app.index is not None else 1
    new_app.index = next_index

    # Create a JWT token for the application/service
    jwt_token = create_application_access_token(app_data.name, new_app.id)
    # Hash the JWT token to secure the JWT token
    new_app.api_key = hash_key_v2(jwt_token)

    # Create the application in the database
    new_app = await Application.create(new_app)

    # Serialize the new application data
    new_app = model_serialize(new_app)

    # Add the JWT token to the response for this first time only display
    new_app["jwt_token"] = jwt_token

    return AppJSONResponse(content={**new_app}, status_code=status.HTTP_201_CREATED)


@router.patch(
    "/delete/{app_id}",
    name="soft_delete_application_route_v2",
    description="Route to soft delete an existing "
    "application/service from the mongo database.",
    operation_id="soft_delete_application_route_v2",
    response_model=Application,
    status_code=status.HTTP_200_OK,
)
async def soft_delete_application(app_id: str) -> AppJSONResponse:
    """
    Delete an existing application/service by its ID.
    """
    logger.info("Deleting application/service with ID %s", app_id)
    app = await Application.find_one(
        Application.id == app_id, Application.deleted_at == None
    )

    if not app:
        logger.warning("Application with ID %s not found.", app_id)
        return AppJSONResponse(
            content={"detail": f"Application ({app_id}) not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Soft delete the application by setting deleted_at timestamp
    app.deleted_at = datetime.now(timezone.utc)
    await app.save()

    return AppJSONResponse(
        content={"detail": f"Application {app_id} soft deleted successfully"},
        status_code=status.HTTP_200_OK,
    )


@router.patch(
    "/{app_id}",
    name="update_application_route_v2",
    description="Route to update an existing application/service "
    "in the mongo database.",
    operation_id="update_application_route_v2",
    response_model=NewApplication,
    status_code=status.HTTP_200_OK,
)
async def patch_update_application(
    app_id: str, app_data: PatchUpdateApplication
) -> AppJSONResponse:
    """
    Update an existing application/service.
    """
    logger.info("Updating application/service with ID %s", app_id)
    app = await Application.find_one(
        Application.id == app_id, Application.deleted_at == None
    )

    if not app:
        logger.warning("Application with ID %s not found.", app_id)
        return AppJSONResponse(
            content={"detail": f"Application ({app_id}) not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Update the application data with the provided attributes
    app_data_dict = app_data.model_dump(exclude_unset=True)
    for key, value in app_data_dict.items():
        setattr(app, key, value)

    # Save updated data & serialize for response
    app.updated_at = datetime.now(timezone.utc)
    app = await app.save()

    return AppJSONResponse(content=model_serialize(app), status_code=status.HTTP_200_OK)


@router.put(
    "/{app_id}",
    name="update_application_put_route_v2",
    description="Route to update an existing application/service "
    "in the mongo database using PUT method.",
    operation_id="update_application_put_route_v2",
    response_model=PutApplicationData,
    status_code=status.HTTP_200_OK,
)
async def put_update_application(
    app_id: str, app_data: PutApplicationData
) -> AppJSONResponse:
    """
    Update an existing application/service using PUT method.
    This method is used to update the application/service data.
    """
    logger.info("Updating application/service with ID %s using PUT", app_id)
    app = await Application.find_one(
        Application.id == app_id, Application.deleted_at == None
    )

    if not app:
        logger.warning("Application with ID %s not found.", app_id)
        return AppJSONResponse(
            content={"detail": f"Application ({app_id}) not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Update the application data with the provided attributes
    app_data_dict = app_data.model_dump(exclude_unset=True)
    for key, value in app_data_dict.items():
        setattr(app, key, value)

    # Save updated data & serialize for response
    app.updated_at = datetime.now(timezone.utc)
    app = await app.save()

    return AppJSONResponse(content=model_serialize(app), status_code=status.HTTP_200_OK)


@router.delete(
    "/delete/{app_id}",
    name="hard_delete_application_route_v2",
    description="Route to hard delete an existing "
    "application/service from the mongo database.",
    operation_id="hard_delete_application_route_v2",
    response_model=Application,
    status_code=status.HTTP_200_OK,
)
async def hard_delete_application(app_id: str) -> AppJSONResponse:
    """
    Hard delete an existing application/service by its ID.
    """
    logger.info("Hard deleting application/service with ID %s", app_id)
    app = await Application.find_one(Application.id == app_id)

    if not app:
        logger.warning("Application with ID %s not found.", app_id)
        return AppJSONResponse(
            content={"detail": f"Application ({app_id}) not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Hard delete the application from the database
    await app.delete()

    return AppJSONResponse(
        content={"detail": f"Application {app_id} deleted successfully"},
        status_code=status.HTTP_200_OK,
    )
