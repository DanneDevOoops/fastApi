#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Write a good module docstring here...
"""

from datetime import datetime, timezone
from typing import List, Optional

from beanie import Document, Indexed
from pydantic import Field

from src.db.models.v2_models.sensor_model_v2 import Sensor
from src.utils.nano_id import generate_nano_id


class Device(Document):
    """
    Device data model for storing device information.
    """
    id: str = Field(alias="_id", default=generate_nano_id,
                    description="unique device identifier")
    name: Indexed(str, unique=True) = Field(
        description="Device name")  # Device name

    description: Optional[str] = Field(
        default="No device description provided.",
        description="Informative but short description of the device.",
        min_length=0, max_length=255)
    sensors: List[Sensor]
    tags: dict = Field(default=dict)

    created_at: datetime = Field(default_factory=lambda: datetime.now(
        timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(
        timezone.utc))
    deleted_at: datetime | None = Field(default=None)

    model_config = {}

    class Settings:
        """
        Settings for the Device model.
        """
        name = "devices"

        def __str__(self):
            """
            String representation of the Device model settings.
            """
            return f"Device Settings: {self.name}"

        def __repr__(self):
            """
            Representation of the Device model settings.
            """
            return f"DeviceSettings(name={self.name})"
