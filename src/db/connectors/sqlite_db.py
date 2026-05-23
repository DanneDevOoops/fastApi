#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
SQLite Database configuration module for the FastAPI application.

This module contains the `SQLiteConnector` class, which manages the SQLite
database connection using SQLAlchemy's asynchronous engine and session maker.
"""

import logging

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from core.custom_exceptions import DatabaseException
from src.core.env_config import get_settings

settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")


class SQLiteConnector:
    """
    A class to manage the SQLite database connection for a FastAPI application.

    This class encapsulates the configuration and management of the SQLite
    database connection using SQLAlchemy's asynchronous engine and session
    maker.

    :ivar DATABASE_URL: The database URL for connecting to SQLite.
    :vartype DATABASE_URL: str
    :ivar sqlite_engine: The SQLAlchemy asynchronous engine for the database.
    :vartype sqlite_engine: AsyncEngine
    :ivar async_session_local: The SQLAlchemy session maker for creating
        async sessions.
    :vartype async_session_local: async_sessionmaker
    """

    def __init__(self, db_path: str | None = None):
        """
        Initialize the SQLiteConnector instance.

        This method sets up the database URL, creates an asynchronous
        database engine, and initializes the asynchronous session maker.

        :param db_path: The file path to the SQLite database.
        :type db_path: str
        """
        logger.info("Initializing SQLite connector...")
        if db_path is None:
            self._database_url = str(settings.sqlite_db_url).replace(
                "sqlite:///",
                "sqlite+aiosqlite:///", 1)

        else:
            self._database_url = db_path.replace(
                "sqlite:///",
                "sqlite+aiosqlite:///", 1)

        logger.info(
            "Using SQLite database file: %s", self._database_url)

        self.sqlite_engine = create_async_engine(self._database_url)
        self.async_session_local = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.sqlite_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_sqlite_db(self) -> AsyncSession:
        """
        Method to get a database session.

        This method does not take any parameters and returns a database
        session.

        :return: A database session.
        :rtype: AsyncSession
        """
        logger.info("Opening a new SQLite database session...")
        async with self.async_session_local() as db:
            try:
                yield db
            except DatabaseException as e:
                logger.error("Error occurred: %s", e)
            finally:
                logger.info("Closing the SQLite database session...")
                await db.close()

    def get_db_url(self) -> str:
        """
        Method to get the SQLite database URL.

        :return: The database URL.
        :rtype: str
        """
        logger.info("Returning the SQLite database URL...")
        return self._database_url
