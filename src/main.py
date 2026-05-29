#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Entry point for the FastAPI application.

This module initializes the FastAPI app, configures middleware, exception
handlers, and includes API routers for different versions and utilities. It
also sets up logging, environment-based settings, and handles application
startup and shutdown via a lifespan context manager.

The application supports CORS, custom authentication, and structured error
handling. To run the server directly, execute this module as the main
program.
"""

import os

from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.auth import get_api_key_v1, get_api_key_v2
from src.api.api_utilities import api_utility_router
from src.api.api_v1 import api_v1_router
from src.api.api_v1_ws_router import api_ws_router
from src.api.api_v2 import api_v2_router
from src.core.app_lifespan import app_lifespan
from src.core.custom_exceptions import (
    AuthException,
    BadRequestException,
    ConflictException,
    DatabaseException,
    HTTPException,
    InternalServerException,
    NotFoundException,
    ValidationException,
)
from src.core.env_config import get_settings
from src.core.exception_handlers import (
    auth_exception_handler,
    bad_request_exception_handler,
    conflict_exception_handler,
    database_exception_handler,
    http_exception_handler,
    internal_server_exception_handler,
    not_found_exception_handler,
    validation_exception_handler,
)
from src.core.logger_config import init_logger
from src.middlewares.gzip import GzipResponseMiddleware
from src.middlewares.logger import LoggerMiddleware
from src.utils.app_constants import REQUEST_HEADERS, REQUEST_METHODS, REQUEST_ORIGINS

settings = get_settings()
logger = init_logger(settings.app_logger_name)

app = FastAPI(
    title="FastAPI application",
    description="This is a description... write something better",
    version="0.0.0",
    openapi_url="/api/openapi.json",
    lifespan=app_lifespan,
    debug=bool(os.getenv("APP_DEBUG", "False")),
)

# Exception handlers
app.add_exception_handler(AuthException, auth_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(ConflictException, conflict_exception_handler)
app.add_exception_handler(DatabaseException, database_exception_handler)
app.add_exception_handler(InternalServerException, internal_server_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Middleware
app.add_middleware(LoggerMiddleware)
if settings.app_gzip_enabled:
    app.add_middleware(
        GzipResponseMiddleware,
        minimum_size=settings.app_gzip_minimum_size,
        compresslevel=settings.app_gzip_compress_level,
    )
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=REQUEST_HEADERS,
    allow_methods=REQUEST_METHODS,
    allow_origins=REQUEST_ORIGINS,
)

# API routers included
app.include_router(api_utility_router)

app.include_router(
    api_v1_router,
    dependencies=[Depends(get_api_key_v1)],
)

app.include_router(api_v2_router, dependencies=[Depends(get_api_key_v2)])

app.include_router(api_ws_router, dependencies=[Depends(get_api_key_v1)])

if __name__ == "__main__":
    import uvicorn

    # Initialize settings from environment configuration
    settings = get_settings()

    # Uvicorn Run Server
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload,
        log_config=uvicorn.config.LOGGING_CONFIG,
    )
