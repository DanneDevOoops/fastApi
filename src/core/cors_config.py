#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module contains the CORS configuration constants for the
FastAPI application.
"""

cors_config = {
    "allowed_origins": [
        "*",
        # This is where you register the allowed origins for the application...
        # "http://localhost:5173",
        # "http://localhost:5174",
        # "http://localhost:5175"
    ],
    "allowed_credentials": True,
    "allowed_methods": ["POST", "GET", "PUT", "PATCH", "DELETE", "OPTIONS"],
    "allowed_headers": ["accept", "content-type", "x-api-key"],
}
