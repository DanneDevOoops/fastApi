#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import asyncio
from unittest.mock import AsyncMock

import pytest

from src.utils.web_socket_connection_manager import WebSocketConnectionManager

pytestmark = pytest.mark.unit


class FakeWebSocket:
    def __init__(self):
        self.accept = AsyncMock()
        self.send_text = AsyncMock()


def test_websocket_connection_manager_flow():
    manager = WebSocketConnectionManager()
    websocket_one = FakeWebSocket()
    websocket_two = FakeWebSocket()

    asyncio.run(manager.connect(websocket_one))
    asyncio.run(manager.connect(websocket_two))

    assert manager.active_connections == [websocket_one, websocket_two]
    websocket_one.accept.assert_awaited_once()
    websocket_two.accept.assert_awaited_once()

    asyncio.run(manager.send_personal_message("hello", websocket_one))
    websocket_one.send_text.assert_awaited_once_with("hello")

    asyncio.run(manager.broadcast("broadcast"))
    websocket_one.send_text.assert_awaited_with("broadcast")
    websocket_two.send_text.assert_awaited_once_with("broadcast")

    manager.disconnect(websocket_one)
    assert manager.active_connections == [websocket_two]
