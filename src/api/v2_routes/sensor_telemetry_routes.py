#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Write a good module docstring here...
"""

import asyncio
import logging

from fastapi import APIRouter, status
from fastapi.responses import Response

from src.core.env_config import get_settings
from src.core.responses import AppJSONResponse
from src.db.models.v2_models.sensor_telemetry_model_v2 import (  # PatchUpdateTelemetryData
    CreateSensorTelemetry,
    FilteredSearchTelemetry,
    SensorTelemetry,
)
from src.db.serializers.v2_serializers.v2_model_serializers import model_serialize

router = APIRouter()
settings = get_settings()
logger = logging.Logger(settings.app_logger_name or "application_logger")


@router.options(
    "",
    name="sensor_telemetry_options_v2",
    description="Handle OPTIONS requests for sensor " "telemetry routes.",
    operation_id="sensor_telemetry_options_v2",
)
async def sensor_telemetry_options_v2() -> Response:
    """
    Handle OPTIONS requests for sensor telemetry routes.
    This is used to support CORS preflight requests.
    """
    logger.debug("Handling OPTIONS request for sensor telemetry routes.")
    return Response(
        headers={"Allow": "GET, POST, PUT, PATCH, DELETE"},
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.get(
    "",
    name="get_all_sensor_telemetry_v2",
    description="Route to request all sensor telemetry data.",
    operation_id="get_all_sensor_telemetry_v2",
    status_code=status.HTTP_200_OK,
)
async def get_all_sensor_telemetry_v2() -> AppJSONResponse:
    """
    Get all sensor telemetry data.
    This is a placeholder function and should be implemented.
    """
    logger.info("Getting all sensor telemetry data...")
    all_sensor_telemetry = await SensorTelemetry.all().to_list()

    return AppJSONResponse(
        content=list(map(model_serialize, all_sensor_telemetry)),
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/{sensor_id}",
    name="get_sensor_telemetry_by_id_v2",
    description="Route to request sensor telemetry data by sensor ID.",
    operation_id="get_sensor_telemetry_by_id_v2",
    status_code=200,
)
async def get_sensor_telemetry_by_id_v2(sensor_id: str) -> Response:
    """
    Get sensor telemetry data by sensor ID.
    This is a placeholder function and should be implemented.
    """
    logger.debug("Getting telemetry data for sensor ID: %s", sensor_id)
    # Placeholder for actual implementation
    return AppJSONResponse(
        content=f"Telemetry data for sensor ID: {sensor_id}",
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "",
    name="create_sensor_telemetry_v2",
    description="Route to create new sensor telemetry data.",
    operation_id="create_sensor_telemetry_v2",
    status_code=status.HTTP_201_CREATED,
)
async def create_sensor_telemetry_v2(
    input_telemetry_data: CreateSensorTelemetry,
) -> AppJSONResponse:
    """
    Create new sensor telemetry data.
    This is a placeholder function and should be implemented.
    """
    logger.debug("Creating new sensor telemetry data...")
    new_telemetry = SensorTelemetry(
        **input_telemetry_data.model_dump(exclude_unset=True)
    )

    new_telemetry_item = await new_telemetry.create()

    return AppJSONResponse(
        content=model_serialize(new_telemetry_item), status_code=status.HTTP_201_CREATED
    )


@router.post(
    "/filtered",
    name="get_filtered_sensor_telemetry_v2",
    description="Route to get filtered sensor telemetry data.",
    operation_id="get_filtered_sensor_telemetry_v2",
    status_code=status.HTTP_200_OK,
)
async def get_filtered_sensor_telemetry_v2(
    filter_params: FilteredSearchTelemetry,
) -> AppJSONResponse:
    """
    Create new sensor telemetry data.
    This is a placeholder function and should be implemented.
    """
    logger.info("Filtering telemetry data with parameters: %s", filter_params)
    print(filter_params.map(lambda x: x))

    # # Check if filter_params contains specific keys
    # if filter_params.get("sensor_id") and filter_params.get("key") and \
    #         filter_params.get("value") and filter_params.get("time"):
    #     logger.debug("Filtering telemetry data with provided parameters.")
    #
    # elif filter_params.get("sensor_id") and filter_params.get(
    #         "key") and filter_params.get("value"):
    #     logger.debug(
    #         "Filtering telemetry data with sensor_id, key, and value.")
    #
    # if not filter_params:
    #     logger.warning("No filter parameters provided.")
    #     return AppJSONResponse(
    #         content={"detail": "No filter parameters provided"},
    #         status_code=status.HTTP_400_BAD_REQUEST
    #     )
    #
    # filtered_telemetry = await SensorTelemetry.filter(
    #     SensorTelemetry.key == filter_params.get("key", None)
    # ).to_list()
    #
    # # Validate filter_params
    # new_telemetry = SensorTelemetry(
    #     **filter_params.model_dump(exclude_unset=True))
    #
    # new_telemetry_item = await new_telemetry.create()

    return AppJSONResponse(
        content=f"Händer det något...? {filter_params}", status_code=status.HTTP_200_OK
    )


@router.patch(
    "/{sensor_id}",
    name="update_sensor_telemetry_v2",
    description="Route to update sensor telemetry data by " "sensor ID.",
    operation_id="update_sensor_telemetry_v2",
    status_code=status.HTTP_200_OK,
)
async def update_sensor_telemetry_v2(
    telemetry_data_id: str,
    # telemetry_data: PathchUpdateTelemetryData
) -> AppJSONResponse:
    """
    Update sensor telemetry data by sensor ID.
    """
    logger.debug("Updating telemetry data for sensor ID: %s", telemetry_data_id)
    telemetry_data_in_db = await SensorTelemetry.find_one(
        SensorTelemetry.sensor_id == telemetry_data_id
    )

    if not telemetry_data_in_db:
        logger.warning("Telemetry data with ID %s not found.", telemetry_data_id)
        return AppJSONResponse(
            content={"detail": "Telemetry data not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.post(
    "/fake_some",
    name="fake_some_sensor_telemetry_v2",
    description="Route to create fake sensor telemetry data.",
    operation_id="fake_some_sensor_telemetry_v2",
    status_code=status.HTTP_201_CREATED,
)
async def fake_some_sensor_telemetry_v2(
    number_of_items: int = 10, interval: int = 1
) -> AppJSONResponse:
    """
    Create fake sensor telemetry data for testing purposes.
    """
    logger.info(
        "Creating %s fake sensor telemetry items with an interval of %s seconds...",
        number_of_items,
        interval,
    )

    created_items = []
    for i in range(number_of_items):
        fake_telemetry = SensorTelemetry(
            key=f"test_value_{i}", value=i * 3.14, sensor_id=f"sensor_id_{i}"
        )

        await fake_telemetry.create()
        created_items.append(model_serialize(fake_telemetry))

        logger.info("Created fake telemetry item %s of %s", (i + 1), number_of_items)

        if i < number_of_items - 1:
            await asyncio.sleep(interval)

    return AppJSONResponse(content=created_items, status_code=status.HTTP_201_CREATED)
