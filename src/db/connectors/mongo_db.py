#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Base module for the database configuration.

This module contains the base class for the database configuration.

The following class is defined:

- Base: The declarative base class for SQLAlchemy.

Each class includes a detailed docstring with information about its purpose.
"""

import logging
from typing import Any, AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from src.core.env_config import get_settings

settings = get_settings()
logger = logging.getLogger(settings.app_logger_name)


class MongoDBConnector:
    """
    Singleton class for managing an asynchronous MongoDB client connection.

    The `MongoDBConnector` ensures only one instance of the async
    `AsyncIOMotorClient` is created and shared throughout the application.
    It provides methods for connecting to MongoDB, retrieving collections,
    testing the connection, and closing the client.

    Example:
        connector = MongoDBConnector(uri)
        collection = connector.get_collection("my_collection")

    .. graphviz::
       :class: MongoDBConnector
       :name: inheritance_diagram_mongodbconnector
       :alt: MongoDBConnector inheritance diagram
       :caption: MongoDBConnector inheritance diagram
       :align: center

        digraph inheritance {
            MongoDBConnector [shape=box, style=filled, fillcolor=lightblue];
            AsyncIOMotorClient [shape=box, style=filled, fillcolor=lightgray];
            MongoDBConnector -> AsyncIOMotorClient [label="uses"];
        }

    .. inheritance-diagram:: MongoDBConnector
       :include-subclasses:
    """
    _instance = None
    _uri = None

    def __new__(cls, uri) -> AsyncIOMotorClient:
        """
        Instantiate or return the singleton MongoDBConnector.

        Ensures that only one instance of the connector exists. If an
        instance does not exist, it initializes the MongoDB client with the
        provided URI.

        :param uri: MongoDB connection URI.
        :type uri: str
        :return: The singleton instance of the connector.
        :rtype: MongoDBConnector
        """
        logger.info("Initializing the MongoDBConnector instance...")

        if cls._instance is None:
            cls._instance = super(MongoDBConnector, cls).__new__(cls)
            cls._uri = uri
            cls._client = AsyncIOMotorClient(cls._uri)

        return cls._instance

    @property
    def client(self):
        """
        Returns the MongoDB client instance.

        :return: The MongoDB client instance.
        :rtype: AsyncIOMotorClient
        """
        return self._client

    async def test_connection(self):
        """
        Asynchronously test the connection to the MongoDB deployment.

        :raises ConnectionFailure: If unable to connect to MongoDB.
        """
        logger.info("Testing the MongoDB Connection...")

        try:
            await self._client.admin.command('ping')
            logger.info("Successfully CONNECTED to MongoDB!")
        except ConnectionFailure:
            logger.error("Failed to connect to MongoDB.")
            raise

    def get_collection(self, collection_name: str):
        """
        Retrieve a MongoDB collection by name.

        :param collection_name: Name of the MongoDB collection to retrieve.
        :type collection_name: str
        :return: The requested MongoDB collection.
        :rtype: Collection
        """
        logger.info("Get MongoDB collection: '%s'", collection_name)
        return self._client.db_name[collection_name]

    async def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        logger.info("Closing MongoDB connection...")
        self._client.close()
        logger.info("MongoDB connection is closed...")


# Register MongoDBConnector as a FastAPI dependency
async def get_mongo_connector() -> AsyncGenerator[AsyncIOMotorClient, Any]:
    """
    Returns the MongoDBConnector instance.

    :return: The MongoDBConnector instance.
    :rtype: MongoDBConnector
    """
    logger.info("Getting the MongoDBConnector instance...")
    mongo_connector = MongoDBConnector(uri=settings.mongo_db_url)
    yield mongo_connector
    mongo_connector.close_connection()
    logger.info("MongoDB connection closed...")
