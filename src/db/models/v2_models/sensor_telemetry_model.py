#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Write a good module docstring here...
"""

from datetime import datetime, timezone

from beanie import Document, Granularity, TimeSeriesConfig
from bson import ObjectId
from pydantic import Field

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
