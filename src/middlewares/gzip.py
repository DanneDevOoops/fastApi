#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods

"""
Gzip response middleware.

This module wraps Starlette's GZip middleware so it can be configured and used
consistently with the rest of this project middleware stack.
"""

from starlette.middleware.gzip import GZipMiddleware


class GzipResponseMiddleware(GZipMiddleware):
    """
    Middleware that compresses eligible HTTP responses using gzip.
    """

    def __init__(self, app, minimum_size: int = 500, compresslevel: int = 9):
        """
        Initialize gzip middleware settings.

        :param app: ASGI application instance.
        :param minimum_size: Minimum number of response bytes before compression.
        :param compresslevel: Gzip compression level (1-9).
        """
        super().__init__(
            app,
            minimum_size=minimum_size,
            compresslevel=compresslevel,
        )
