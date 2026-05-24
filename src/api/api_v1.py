#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
API v1 Router

This module defines the API v1 router for the FastAPI application. It
includes all routes interacting with the PostgreSQL database. The router
is included in the main FastAPI application instance in the src/main.py
module.
"""

from fastapi import APIRouter

from src.api.v1_routes import application_routes, user_routes

api_v1_router = APIRouter(
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)

api_v1_router.include_router(
    application_routes.router,
    prefix="/applications",
    tags=["applications"],
    # dependencies=[Depends(get_api_key_v1)],
)

api_v1_router.include_router(
    user_routes.router,
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_api_key_v1)],
)
