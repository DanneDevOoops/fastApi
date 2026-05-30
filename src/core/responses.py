#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom response classes for the FastAPI application.
"""

import orjson  # pylint: disable=no-member
from starlette.responses import Response


class AppJSONResponse(Response):
    """Custom JSON response using orjson for datetime-aware serialization."""

    media_type = "application/json"

    def render(self, content) -> bytes:
        return orjson.dumps(content)  # pylint: disable=no-member
