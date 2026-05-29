#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import pytest

pytestmark = pytest.mark.integration


def test_websocket_route(client):
    with client.websocket_connect("/api/v1/ws/123") as websocket:
        websocket.send_text("hello")
        assert websocket.receive_text() == "You wrote: hello"
        assert websocket.receive_text() == "Client #123 says: hello"


def test_websocket_html_page(client):
    response = client.get("/api/v1/ws/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_websocket_broadcast(client):
    with client.websocket_connect("/api/v1/ws/1") as ws1:
        with client.websocket_connect("/api/v1/ws/2") as ws2:
            ws1.send_text("hello")
            assert ws1.receive_text() == "You wrote: hello"
            assert ws1.receive_text() == "Client #1 says: hello"
            assert ws2.receive_text() == "Client #1 says: hello"
