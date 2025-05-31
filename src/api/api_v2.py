#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module defines the User API routes for the FastAPI application.
"""

from fastapi import APIRouter

from src.api.v2_routes import user_routes

api_v2_router = APIRouter(
    prefix="/api/v2",
    responses={
        404: {"description": "Not found"}
    },
)

api_v2_router.include_router(
    user_routes.router,
    prefix="/users",
    tags=["users"],
)
