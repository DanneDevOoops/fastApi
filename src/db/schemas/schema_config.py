#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module contains the schema configurations for database models.
"""

from pydantic import ConfigDict

standard_model_config = ConfigDict(
    from_attributes=True,
    str_strip_whitespace=True,
    arbitrary_types_allowed=True,
    str_min_length=1,
    str_max_length=255,
)
