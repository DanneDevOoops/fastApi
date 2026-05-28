#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file


def test_websocket_route(client):
    with client.websocket_connect("/api/v1/ws/123") as websocket:
        websocket.send_text("hello")
        assert websocket.receive_text() == "You wrote: hello"
        assert websocket.receive_text() == "Client #123 says: hello"
