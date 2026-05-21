#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Postgres Database configuration module for the FastAPI application.

This module contains the `PostgresConnector` class, which manages the
PostgreSQL database connection using SQLAlchemy's asynchronous engine and
session maker.
"""

import logging
from asyncio import current_task
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)

from src.core.custom_exceptions import DatabaseException
from src.core.env_config import get_settings

settings = get_settings()
logger = logging.getLogger(settings.app_logger_name)


class PgsqlDbSessionManager:
    """
    A session manager class for the Postgres database connection within a
    FastAPI application. This class manages the creation and disposal of
    asynchronous database sessions using SQLAlchemy.
    """

    def __init__(self, db_connection_str: str = None):
        """
        Constructor method for the PgsqlDbSessionManager class to
        initialize the database connection instance.

        This method sets up the database connection string, creates the
        asynchronous database engine, session maker, and scoped session.

        :param db_connection_str: The database connection string.
        :type db_connection_str: str
        """
        logger.info("Initializing the PgsqlDbSessionManager instance...")

        # Set the database connection string based on the environment
        # settings or a provided case specific connector string...
        if db_connection_str is None:
            logger.info("Using the default database connection string...")
            self._postgres_database_url = (
                str(settings.pg_db_url).replace(
                    "postgresql://", "postgresql+asyncpg://"))
        else:
            logger.info("Using the provided database connection string...")
            self._postgres_database_url = db_connection_str.replace(
                "postgresql://", "postgresql+asyncpg://")

        # Create the async database engine...
        logger.info("Creating the async database engine...")
        self.pgsql_db_engine = create_async_engine(
            self._postgres_database_url,
            future=settings.pg_db_future,
            echo=settings.pg_db_echo,
            pool_size=settings.pg_db_connection_pool_size,
            max_overflow=settings.pg_db_max_overflow,
        )

        # Create the async session maker...
        logger.info("Creating the async session maker...")
        self.session_maker = async_sessionmaker(
            autocommit=settings.pg_db_auto_commit,
            autoflush=settings.pg_db_auto_flush,
            bind=self.pgsql_db_engine,
            class_=AsyncSession,
            expire_on_commit=settings.pg_db_expire_on_commit,
        )

        # Create the scoped session...
        logger.info("Creating the scoped session...")
        self.scoped_session = async_scoped_session(
            self.session_maker,
            scopefunc=current_task,
        )

    def get_session(self) -> AsyncSession:
        """
        Get a new asynchronous database session.

        :return: A new asynchronous database session.
        :rtype: AsyncSession
        """
        return self.session_maker()

    async def close_session(self):
        """
        Close the asynchronous database session. This method disposes of
        the database engine, effectively closing all active sessions.

        :raises DatabaseException: If the database engine is not initialized.
        :return: None
        """
        if self.pgsql_db_engine is not None:
            raise DatabaseException("Database engine is not initialized...")
        await self.pgsql_db_engine.dispose()

    @staticmethod
    def get_db_connection_str() -> str:
        """
         Get the Postgres database connection string.

        :return: The Postgres database connection string.
        :rtype: str
        """
        return f"""
        dbname={settings.pg_db_name}
        user={settings.pg_db_username}
        password={settings.pg_db_password}
        host={settings.pg_db_host}
        port={settings.pg_db_port}
        """


# Initialize the PgsqlDbSessionManager instance
session_manager = PgsqlDbSessionManager()


async def get_pg_db() -> AsyncIterator[AsyncSession]:
    """
    Get a new session for the database. This method retrieves a new
    asynchronous database session from the session manager. If the session
    manager is not initialized correctly, it raises a DatabaseException.

    :raises DatabaseException: If the PgsqlDbSessionManager is not
        initialized correctly.
    :yield: A new asynchronous database session.
    :rtype: AsyncIterator[AsyncSession]
    """
    session = session_manager.get_session()
    if session is None:
        raise DatabaseException(
            "PgsqlDbSessionManager is not initialized correctly...")
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
