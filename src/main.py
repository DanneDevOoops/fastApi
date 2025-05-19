#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module is the main entry point of the FastAPI application.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from psycopg_pool import AsyncConnectionPool
from starlette.middleware.cors import CORSMiddleware

from src.api.api_utilities import api_utility_router
from src.api.api_v1 import api_v1_router
from src.api.api_v1_ws_router import api_ws_router
from src.core.auth import get_api_key
from src.core.custom_exceptions import AuthException, BadRequestException, \
    ConflictException, DatabaseException, InternalServerException, \
    NotFoundException, ValidationException, HTTPException
from src.core.env_config import get_settings
from src.core.exception_handlers import auth_exception_handler, \
    bad_request_exception_handler, conflict_exception_handler, \
    database_exception_handler, http_exception_handler, \
    internal_server_exception_handler, not_found_exception_handler, \
    validation_exception_handler
from src.core.logger_config import init_logger
from src.db.connectors.mongo_db import MongoDBConnector
from src.db.connectors.postgres_db import PgsqlDbSessionManager
from src.middlewares.logger import LoggerMiddleware
from src.utils.app_constants import REQUEST_HEADERS, REQUEST_METHODS, \
    REQUEST_ORIGINS

# Initialize settings from environment configuration
settings = get_settings()

# Initialize the loggers
logger = init_logger(settings.app_logger_name)


@asynccontextmanager
async def app_lifespan(app_instance: FastAPI):
    """
    Lifespan context manager for the FastAPI application instance.
    """
    logger.info("Application lifespan started...")

    # Initialize the application settings
    logger.info("Initializing the FastAPI application...")
    app_instance.settings = settings

    # Initialize the database connector instances
    logger.info("Initializing the database managers...")
    postgres_connector = PgsqlDbSessionManager()
    mongo_connector = MongoDBConnector(uri=settings.mongo_db_url)

    # sqlite_connector = SQLiteConnector()

    # Initialize the database connection pool
    logger.info("Initializing the async database connection pool...")
    app_instance.async_pool = AsyncConnectionPool(
        conninfo=postgres_connector.get_db_connection_str()
    )

    logger.info("Application lifespan startup completed...")

    yield  # API runtime

    logger.info("Shutting down the FastAPI application...")

    # Close the database connection pool
    logger.info("Closing the database session managers...")
    await app_instance.async_pool.close()
    await mongo_connector.close_connection()

    logger.info("Application lifespan shutdown completed...")


# Create FastAPI instance with lifespan context manager
app = FastAPI(
    title="FastAPI application",
    description="This is a description... write something better",
    version="0.0.0",
    openapi_url="/api/openapi.json",
    lifespan=app_lifespan,
    debug=bool(os.getenv("APP_DEBUG", 'False'))
)

# Exception handlers
app.add_exception_handler(AuthException, auth_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(ConflictException, conflict_exception_handler)
app.add_exception_handler(DatabaseException, database_exception_handler)
app.add_exception_handler(InternalServerException,
                          internal_server_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Middleware
app.add_middleware(LoggerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=REQUEST_HEADERS,
    allow_methods=REQUEST_METHODS,
    allow_origins=REQUEST_ORIGINS,
)

# API routers included
app.include_router(
    api_utility_router
)

app.include_router(
    api_v1_router,
    dependencies=[Depends(get_api_key)]
)

app.include_router(
    api_ws_router,
    dependencies=[Depends(get_api_key)]
)

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
        log_config=uvicorn.config.LOGGING_CONFIG
    )
