#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Write a good module docstring here...
"""

from datetime import datetime, timezone
from typing import Optional

from beanie import Document, Granularity, TimeSeriesConfig
from bson import ObjectId
from pydantic import BaseModel, Field

from src.utils.nano_id import generate_nano_id


class SensorTelemetry(Document):
    """
    Sensor reading data model for time series data.
    """
    id: str = Field(alias="_id", default_factory=generate_nano_id,
                    description="unique sensor reading identifier")
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    key: str  # Sensor name/type
    value: float = Field(default=0.0)
    sensor_id: str

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the SensorReading model.
        """
        name = "sensor_telemetry"
        timeseries = TimeSeriesConfig(
            time_field="time",
            meta_field="device_id",
            granularity=Granularity.seconds,
        )

        def __str__(self):
            """
            String representation of the SensorReading model settings.
            """
            return f"Sensor: {self.name}"

        def __dir__(self):
            """
            List of attributes for the SensorReading model settings.
            """
            return self.__dict__.keys()


class CreateSensorTelemetry(BaseModel):
    """
    CreateSensorTelemetry class.
    """
    key: str
    value: float = Field(default=0.0)
    sensor_id: str

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the SensorReading model.
        """
        name = "sensor_telemetry"
        timeseries = TimeSeriesConfig(
            time_field="time",
            meta_field="device_id",
            granularity=Granularity.seconds,
        )

        def __str__(self):
            """
            String representation of the SensorReading model settings.
            """
            return f"Sensor: {self.name}"

        def __dir__(self):
            """
            List of attributes for the SensorReading model settings.
            """
            return self.__dict__.keys()


class PathchUpdateTelemetryData(BaseModel):
    """
    Model for patching/updating telemetry data.
    """
    key: str | None = None
    value: float | None = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the PatchUpdateTelemetryData model.
        """
        name = "patch_update_telemetry_data"

        def __str__(self):
            """
            String representation of the PatchUpdateTelemetryData
            model settings.
            """
            return f"Patch Update Telemetry Data: {self.name}"

        def __dir__(self):
            """
            List of attributes for the PatchUpdateTelemetryData model settings.
            """
            return self.__dict__.keys()


class FilteredSearchTelemetry(BaseModel):
    """
    Model for patching/updating telemetry data.
    """
    sensor_id: Optional[str] = None
    key: Optional[str] = None
    value: Optional[float] = None
    time_span_start: Optional[str] = None
    time_span_end: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    class Settings:
        """
        Settings for the PatchUpdateTelemetryData model.
        """
        name = "patch_update_telemetry_data"

        def __str__(self):
            """
            String representation of the PatchUpdateTelemetryData
            model settings.
            """
            return f"Patch Update Telemetry Data: {self.name}"

        def __dir__(self):
            """
            List of attributes for the PatchUpdateTelemetryData model settings.
            """
            return self.__dict__.keys()
