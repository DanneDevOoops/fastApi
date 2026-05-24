#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=singleton-comparison


"""
Implements FastAPI routes for sensor management in API v2.

Includes endpoints for creating sensors, retrieving single or multiple sensors
(active and soft deleted), updating sensor data (partial and full),
soft deleting sensors, and permanently deleting sensors from the MongoDB
database. Each route handles request validation, response formatting,
and logging as appropriate.
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse, Response

from src.core.env_config import get_settings
from src.db.models.v2_models.sensor_model_v2 import (
    CreateSensor,
    PatchSensorData,
    PutUpdateSensorData,
    Sensor,
)
from src.db.serializers.v2_serializers.v2_model_serializers import model_serialize

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")


@router.options("", operation_id="options_sensor_routes_v2")
def sensor_routes_options_v2() -> Response:
    """
    Handle OPTIONS requests for the sensor routes.

    This is used to support CORS preflight requests and provides
    information about the allowed HTTP methods for the sensor routes.
    """
    return Response(
        content={"Allow": "GET, POST, PUT, PATCH, DELETE"},
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.get(
    "",
    name="get_all_sensors_route_v2",
    description="Route to get all sensors.",
    operation_id="get_all_sensors_route_v2",
    response_model=list[Sensor],
    status_code=status.HTTP_200_OK,
)
async def get_sensors() -> ORJSONResponse:
    """
    Retrieve all sensors.

    Returns a list of all sensors that have not been soft deleted (i.e.,
    have a null `deleted_at` field). If no sensors are found, returns a 404
    error response.

    :return: A list of sensor data, or a 404 error if none are found.
    :rtype: ORJSONResponse
    """
    all_sensors = await Sensor.find(Sensor.deleted_at == None).to_list()
    if not all_sensors:
        logger.warning("No sensors found.")
        return ORJSONResponse(
            content={"detail": "No sensors found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ORJSONResponse(
        content=list(map(model_serialize, all_sensors)), status_code=status.HTTP_200_OK
    )


@router.get(
    "/deleted",
    name="get_soft_deleted_sensors_route_v2",
    description="Route to get all soft deleted sensors.",
    operation_id="get_soft_deleted_sensors_route_v2",
    response_model=Sensor,
    status_code=status.HTTP_200_OK,
)
async def get_all_soft_deleted_sensors() -> ORJSONResponse:
    """
    Retrieve all soft deleted sensors.

    Returns a list of sensors that have been soft deleted (i.e., have a
    non-null `deleted_at` field). If no soft deleted sensors are found,
    returns a 404 error response.

    :return: A list of soft deleted sensor data, or a 404 error if none
        are found.
    :rtype: ORJSONResponse
    """
    soft_deleted_sensors = await Sensor.find(Sensor.deleted_at != None).to_list()
    if not soft_deleted_sensors:
        return ORJSONResponse(
            content={"detail": "No soft deleted sensors found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ORJSONResponse(
        content=list(map(model_serialize, soft_deleted_sensors)),
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/{sensor_id}",
    name="get_sensor_by_id_route_v2",
    description="Route to get a sensor by ID.",
    operation_id="get_sensor_by_id_route_v2",
    response_model=Sensor,
    status_code=status.HTTP_200_OK,
)
async def get_sensor_by_id(sensor_id: str) -> ORJSONResponse:
    """
    Retrieve a sensor by its unique ID.

    Returns the sensor data for the specified ID if it exists and has not
    been soft deleted. If the sensor does not exist, returns a 404 error
    response.

    :param sensor_id: The unique identifier of the sensor to retrieve.
    :type sensor_id: str
    :return: The sensor data if found, or a 404 error if not found.
    :rtype: ORJSONResponse
    """
    sensor = await Sensor.find(
        Sensor.id == sensor_id, Sensor.deleted_at == None
    ).first_or_none()
    if not sensor:
        logger.warning("Sensor with ID %s not found.", sensor_id)
        return ORJSONResponse(
            content={"detail": "Sensor not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ORJSONResponse(
        content=model_serialize(sensor), status_code=status.HTTP_200_OK
    )


@router.post(
    "",
    name="create_sensor_route_v2",
    description="Route to create a new sensor.",
    operation_id="create_sensor_route_v2",
    response_model=Sensor,
    status_code=status.HTTP_201_CREATED,
)
async def create_sensor(sensor_data: CreateSensor) -> ORJSONResponse:
    """
    Create a new sensor.

    Adds a new sensor to the database with a unique index. The index is set
    to one higher than the current maximum. Returns the created sensor data.

    :param sensor_data: The data required to create the new sensor.
    :type sensor_data: CreateSensor
    :return: The newly created sensor data.
    :rtype: ORJSONResponse
    """
    # Find the current max index
    last_sensor = await Sensor.find().sort("-index").first_or_none()
    next_index = (
        (last_sensor.index + 1) if last_sensor and last_sensor.index is not None else 1
    )

    # Create the Sensor with the required index
    new_sensor = Sensor(index=next_index, **sensor_data.model_dump())
    new_sensor = await new_sensor.create()

    return ORJSONResponse(
        content=model_serialize(new_sensor), status_code=status.HTTP_201_CREATED
    )


@router.patch(
    "/delete/{sensor_id}",
    name="soft_delete_sensor_route_v2",
    description="Route to soft delete a sensor by ID.",
    operation_id="soft_delete_sensor_route_v2",
    response_model=Sensor,
    status_code=status.HTTP_200_OK,
)
async def soft_delete_sensor_v2(sensor_id: str) -> ORJSONResponse:
    """
    Soft delete a sensor by its unique ID.

    Marks the specified sensor as deleted by setting its `deleted_at`
    timestamp. If the sensor does not exist or is already deleted, returns
    a 404 error response.

    :param sensor_id: The unique identifier of the sensor to soft delete.
    :type sensor_id: str
    :return: The updated sensor data with the `deleted_at` field set,
        or a 404 error if not found.
    :rtype: ORJSONResponse
    """
    sensor = await Sensor.find_one(Sensor.id == sensor_id, Sensor.deleted_at == None)

    if not sensor:
        logger.warning("Sensor with ID %s not found or already marked as deleted.", sensor_id)
        return ORJSONResponse(
            content={"detail": "Sensor not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Set the deleted_at field to the current time
    sensor.updated_at = datetime.now(timezone.utc)
    sensor.deleted_at = datetime.now(timezone.utc)
    sensor_updated = await sensor.save()

    return ORJSONResponse(
        content=model_serialize(sensor_updated), status_code=status.HTTP_200_OK
    )


@router.patch(
    "/{sensor_id}",
    name="update_sensor_route_v2",
    description="Route to update a sensor by ID.",
    operation_id="update_sensor_route_v2",
    response_model=Sensor,
    status_code=status.HTTP_200_OK,
)
async def patch_update_sensor_v2(
    sensor_id: str, sensor_data: PatchSensorData
) -> ORJSONResponse:
    """
    Partially update a sensor by its unique ID.

    Updates one or more fields of the specified sensor with the provided
    data. If the sensor does not exist or has been soft deleted, returns a
    404 error response.

    :param sensor_id: The unique identifier of the sensor to update.
    :type sensor_id: str
    :param sensor_data: The partial set of sensor data to update.
    :type sensor_data: PatchSensorData
    :return: The updated sensor data if successful, or a 404 error if
        not found.
    :rtype: ORJSONResponse
    """
    sensor = await Sensor.find(
        Sensor.id == sensor_id, Sensor.deleted_at == None
    ).first_or_none()
    if not sensor:
        logger.warning("Sensor with ID %s not found.", sensor_id)
        return ORJSONResponse(
            content={"detail": "Sensor not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Update the sensor with the provided data
    sensor_data_dict = sensor_data.model_dump(exclude_unset=True)
    for key, value in sensor_data_dict.items():
        setattr(sensor, key, value)

    sensor.updated_at = datetime.now(timezone.utc)
    sensor_updated = await sensor.save()

    return ORJSONResponse(
        content=model_serialize(sensor_updated), status_code=status.HTTP_200_OK
    )


@router.put(
    "/{sensor_id}",
    name="update_sensor_full_route_v2",
    description="Route to fully update a sensor by ID.",
    operation_id="update_sensor_full_route_v2",
    response_model=Sensor,
    status_code=status.HTTP_200_OK,
)
async def update_sensor_full_route_v2(
    sensor_id: str, sensor_data: PutUpdateSensorData
) -> ORJSONResponse:
    """
    Fully update a sensor by its unique ID.

    Replaces all fields of the specified sensor with the provided data. If
    the sensor does not exist or has been soft deleted, returns a 404 error
    response.

    :param sensor_id: The unique identifier of the sensor to update.
    :type sensor_id: str
    :param sensor_data: The complete set of new sensor data.
    :type sensor_data: PutUpdateSensorData
    :return: The updated sensor data if successful, or a 404 error if
        not found.
    :rtype: ORJSONResponse
    """
    sensor = await Sensor.find_one(Sensor.id == sensor_id, Sensor.deleted_at == None)

    if not sensor:
        logger.warning("Sensor with ID %s not found.", sensor_id)
        return ORJSONResponse(
            content={"detail": "Sensor not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Update the sensor with the provided data
    sensor_data_dict = sensor_data.model_dump(exclude_unset=True)
    for key, value in sensor_data_dict.items():
        setattr(sensor, key, value)

    sensor.updated_at = datetime.now(timezone.utc)
    sensor_updated = await sensor.save()

    return ORJSONResponse(
        content=model_serialize(sensor_updated), status_code=status.HTTP_200_OK
    )


@router.delete(
    "/delete/{sensor_id}",
    name="delete_sensor_route_v2",
    description="Route to delete a sensor by ID.",
    operation_id="delete_sensor_route_v2",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_sensor(sensor_id: str) -> ORJSONResponse:
    """
    Delete a sensor by its unique ID.

    Permanently removes the sensor from the database. If the sensor does
    not exist, returns a 404 error response.

    :param sensor_id: The unique identifier of the sensor to delete.
    :type sensor_id: str
    :return: An empty response with HTTP 204 status if successful, or a 404
        error if not found.
    :rtype: ORJSONResponse
    """
    sensor = await Sensor.find_one(Sensor.id == sensor_id)
    if not sensor:
        logger.warning("Sensor with ID %s not found.", sensor_id)
        return ORJSONResponse(
            content={"detail": "Sensor not found."},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    await sensor.delete()

    return ORJSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
