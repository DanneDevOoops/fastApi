#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module contains the WebSockets for the application.
"""

import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from src.core.env_config import get_settings
from src.utils.web_socket_connection_manager import WebSocketConnectionManager

# Initialize environment settings & logger
settings = get_settings()
logger = logging.getLogger(settings.app_logger_name or "application_logger")

ws_router = APIRouter()
socket_manager = WebSocketConnectionManager()

HTML = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:1337/api/v1/ws/${
            client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@ws_router.get("/")
async def get() -> HTMLResponse:
    """
    Handles the GET request for the WebSocket endpoint.

    :return: The HTML response.
    :rtype: HTMLResponse
    """
    return HTMLResponse(HTML)


@ws_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int) -> None:
    """
    Handles the WebSocket connection endpoint.

    :param websocket: The WebSocket connection.
    :type websocket: WebSocket

    :param client_id: The client ID.
    :type client_id: int

    :return: This function does not return anything.
    :rtype: None
    """
    await socket_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await socket_manager.send_personal_message(f"You wrote: {data}", websocket)
            await socket_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        socket_manager.disconnect(websocket)
        await socket_manager.broadcast(f"Client #{client_id} left the chat")
