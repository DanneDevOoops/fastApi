#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Write a good module docstring here...
"""

from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool

from src.core.env_config import get_settings
from src.core.logger_config import init_logger
from src.db.connectors.mongo_db import MongoDBConnector
from src.db.connectors.postgres_db import PgsqlDbSessionManager
from src.db.models.v2_models.application_model_v2 import Application
from src.db.models.v2_models.device_model_v2 import Device
from src.db.models.v2_models.sensor_model_v2 import Sensor
from src.db.models.v2_models.sensor_telemetry_model_v2 import SensorTelemetry
from src.db.models.v2_models.user_model_v2 import User

# Initialize settings from environment configuration
settings = get_settings()

# Initialize the loggers
logger = init_logger(settings.app_logger_name)

# Here is where you initialization mongo db models
BEANIE_DOCUMENT_MODELS = [
    Application,
    Device,
    Sensor,
    SensorTelemetry,
    User
]


@asynccontextmanager
async def app_lifespan(app_instance: FastAPI):
    """
    Lifespan context manager for the FastAPI application instance.
    """
    logger.info("Application lifespan started...")

    # Initialize the application environment settings ------------------------
    logger.info("Initializing the FastAPI application environment...")
    app_instance.settings = settings

    # Initialize the database connector instances ----------------------------
    logger.info("Initializing the database connectors...")
    postgres_connector = PgsqlDbSessionManager()
    mongo_connector = MongoDBConnector(
        uri=settings.mongo_db_url,
        db_name=settings.mongo_db_name
    )
    app_instance.mongo_connector = mongo_connector

    # Initialize Beanie & register document models ---------------------------
    logger.info("Initializing Beanie document models...")
    for document_model in BEANIE_DOCUMENT_MODELS:
        logger.info("Init model %s...", document_model.Settings.name)

    await init_beanie(
        database=mongo_connector.db,
        document_models=BEANIE_DOCUMENT_MODELS
    )

    # Initialize the database connection pool --------------------------------
    logger.info("Initializing the async database connection pool...")
    app_instance.async_pool = AsyncConnectionPool(
        conninfo=postgres_connector.get_db_connection_str()
    )

    logger.info("Application lifespan startup sequence completed...")

    yield  # API runtime -----------------------------------------------------

    logger.info("Shutting down the FastAPI application...")

    # Close the database connection pool -------------------------------------
    logger.info("Closing the database session connectors...")
    await app_instance.async_pool.close()
    await mongo_connector.close()

    logger.info("Application lifespan shutdown sequence completed...")
