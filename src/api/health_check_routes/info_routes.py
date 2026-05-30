#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Write a good module docstring here...
"""

import logging

from fastapi import APIRouter, status

from src.core.env_config import get_settings
from src.core.responses import AppJSONResponse

info_router = APIRouter()
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")


@info_router.get("/info")
async def info() -> AppJSONResponse:
    """
    Information endpoint to provide application details.

    :return: JSON response with application information
    :rtype: AppJSONResponse
    """
    app_info = {
        "name": settings.app_name,
        "python-version": settings.pyenv_version,
        "description": settings.app_name + " ...some description here...",
        "environment": settings.env_name,
    }

    logger.info("Application info requested: %s", app_info)

    return AppJSONResponse(status_code=status.HTTP_200_OK, content=app_info)


@info_router.get("/pgsql_db_info")
async def pgsql_db_info() -> AppJSONResponse:
    """
    Information endpoint to provide postgres database information details.

    :return: JSON response with postgres database information
    :rtype: AppJSONResponse
    """
    pgsql_info = {
        "name": settings.pg_db_name,
        "python-version": settings.pyenv_version,
        "description": settings.pg_db_name + "some description here...",
        "environment": settings.env_name,
    }

    logger.info("Postgres database info requested: %s", pgsql_info)

    return AppJSONResponse(status_code=status.HTTP_200_OK, content=pgsql_info)


@info_router.get("/mongo_db_info")
async def mongo_db_info() -> AppJSONResponse:
    """
    Information endpoint to provide mongo db information details.

    :return: JSON response with mongo database information
    :rtype: AppJSONResponse
    """
    mongo_info = {
        "name": settings.mongo_db_name,
        "version": settings.mongo_db_name,
        "description": settings.mongo_db_name + "some description here...",
        "environment": settings.pyenv_version,
    }

    logger.info("Mongo database info requested: %s", mongo_info)

    return AppJSONResponse(status_code=status.HTTP_200_OK, content=mongo_info)
