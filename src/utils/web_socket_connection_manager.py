#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module containing a WebSocket connection manager class. This class is
initialized in the router module and used in routes where WebSocket
are needed to manage the connections for broadcasting messages to all
active clients.
"""

import logging

from fastapi import WebSocket

from src.core.env_config import get_settings

# Initialize environment settings & logger
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")


class WebSocketConnectionManager:
    """
    Manages the WebSocket connections
    """

    def __init__(self):
        """
        Initializes the WebSocket connection manager class.
        """
        logger.info("Initializing the WebSocket connection manager...")
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        Connects a WebSocket connection.

        :param websocket: The WebSocket connection to be connected.
        :type websocket: WebSocket
        """
        logger.info("WebSocket connection requested...")
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Disconnects a WebSocket connection.

        :param websocket: The WebSocket connection to be disconnected.
        :type websocket: WebSocket
        """
        logger.info("WebSocket connection closed...")
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """
        Sends a personal message to a specific WebSocket connection.

        :param message: The message to be sent.
        :type message: str
        :param websocket: The WebSocket connection to send the message to.
        :type websocket: WebSocket
        """
        logger.info("Sending personal message over web socket...")
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        """
        Broadcasts a message to all active WebSocket connections.

        :param message: The message to be broadcasted.
        :type message: str
        """
        logger.info("Broadcasting message...")
        for connection in self.active_connections:
            logger.info("Sending message to connection...")
            await connection.send_text(message)
        logger.info("Broadcast completed.")
