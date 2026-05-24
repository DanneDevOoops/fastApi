#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Write a good module docstring here...
"""

from datetime import datetime, timezone
from typing import Optional

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import BaseModel, Field

from src.utils.nano_id import generate_nano_id


class Sensor(Document):
    """
    Sensor information data model for storing sensor details.
    """

    id: str = Field(
        alias="_id",
        default_factory=generate_nano_id,
        description="unique sensor identifier",
    )
    index: Indexed(int, unique=True)
    name: str
    value_unit: str  # Unit to describe the sensor reading value
    location: Optional[str] = "Unknown location"
    device_id: str  # Reference to Device

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = Field(default=None)

    model_config = {"arbitrary_types_allowed": True, "json_encoders": {ObjectId: str}}

    class Settings:
        """
        Settings for the SensorReading model.
        """

        name = "sensors"

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


class CreateSensor(BaseModel):
    """
    Pydantic model for creating a new sensor.
    """

    name: str
    value_unit: str
    location: Optional[str] = "Unknown location"
    device_id: str  # Reference to Device


class PatchSensorData(BaseModel):
    """
    Patch data model for updating sensor information.
    """

    name: Optional[str] = None
    value_unit: Optional[str] = None
    location: Optional[str] = None
    device_id: Optional[str] = None

    class Settings:
        """
        Pydantic settings.
        """

        name = "sensors"

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


class PutUpdateSensorData(BaseModel):
    """
    Full update data model for sensor information.
    """

    name: str
    value_unit: str
    location: str
    device_id: Optional[str] = None  # Reference to Device

    class Settings:
        """
        Pydantic settings.
        """

        name = "sensors"

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
