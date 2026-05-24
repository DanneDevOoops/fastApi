#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module defines the User API routes for the FastAPI application.
"""

from fastapi import APIRouter

from src.api.v2_routes import (
    application_routes,
    auth_routes,
    sensor_routes,
    sensor_telemetry_routes,
    user_routes,
)

api_v2_router = APIRouter(
    prefix="/api/v2",
    responses={404: {"description": "Not found"}},
)

# Included routers in api/v2
api_v2_router.include_router(
    application_routes.router,
    prefix="/applications",
    tags=["applications"],
)

api_v2_router.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["auth"],
)

api_v2_router.include_router(
    sensor_routes.router,
    prefix="/sensors",
    tags=["sensors"],
)

api_v2_router.include_router(
    sensor_telemetry_routes.router,
    prefix="/sensor_telemetry",
    tags=["sensor_telemetry"],
)

api_v2_router.include_router(
    user_routes.router,
    prefix="/users",
    tags=["users"],
)
