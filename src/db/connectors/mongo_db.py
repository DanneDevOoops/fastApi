#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
MongoDB connection utilities using Motor.

This module provides a connector class for managing asynchronous MongoDB
connections with Motor, including access to the client and database
instances, and proper connection cleanup.

Classes:
- MongoDBConnector: Handles connection setup, access, and teardown
    for MongoDB.
"""

import logging

from motor.motor_asyncio import AsyncIOMotorClient

from src.core.env_config import get_settings

settings = get_settings()
logger = logging.getLogger(settings.app_logger_name)


class MongoDBConnector:
    """
    Handles MongoDB connections using Motor.

    Provides methods to initialize a connection, access the client and
    database, and close the connection cleanly.
    """

    def __init__(self, uri: str, db_name: str):
        """
        Initialize the MongoDBConnector.

        Establishes a connection to the MongoDB instance using the provided
        URI and database name.

        :param uri: The MongoDB connection URI.
        :type uri: str
        :param db_name: The name of the MongoDB database to use.
        :type db_name: str
        """
        logger.info("Initializing MongoDB connection...")
        self._client = AsyncIOMotorClient(uri)
        self._db = self._client[db_name]

    @property
    def client(self):
        """
        Get the MongoDB client instance.

        :return: The Motor async MongoDB client.
        :rtype: AsyncIOMotorClient
        """
        return self._client

    @property
    def db(self):
        """
        Get the MongoDB database instance.

        :return: The Motor async MongoDB database.
        :rtype: motor.motor_asyncio.AsyncIOMotorDatabase
        """
        return self._db

    async def close(self):
        """
        Close the MongoDB client connection.

        Shuts down the Motor client and releases all resources.
        """
        logger.info("Closing MongoDB connection...")
        self._client.close()
        logger.info("MongoDB connection closed successfully.")
