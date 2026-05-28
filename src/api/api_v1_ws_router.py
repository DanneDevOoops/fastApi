#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
API Web Sockets Router

This module defines the API v1 router for the FastAPI application. It
includes all routes interacting through web sockets. The router
is included in the main FastAPI application instance in the src/main.py
module.
"""

from fastapi import APIRouter

from src.api.v1_routes.web_socket_routes import ws_router

api_ws_router = APIRouter(
    prefix="/api/v1",
    # dependencies=[Depends(get_api_key_v1)],
    responses={404: {"description": "Not found"}},
)

api_ws_router.include_router(ws_router, prefix="/ws", tags=["web_sockets"])
