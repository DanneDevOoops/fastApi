#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

import hashlib

import pytest
from bson import ObjectId

from src.utils import nano_id

pytestmark = pytest.mark.unit


def test_generate_nano_id_uses_env_values(monkeypatch):
    calls = {}

    def fake_generate(characters, size):
        calls["characters"] = characters
        calls["size"] = size
        return "x" * size

    monkeypatch.setenv("NANO_ID_CHARACTERS", "abc")
    monkeypatch.setenv("NANO_ID_SIZE", "7")
    monkeypatch.setattr(nano_id, "generate", fake_generate)

    assert nano_id.generate_nano_id() == "xxxxxxx"
    assert calls == {"characters": "abc", "size": 7}
    assert nano_id.generate_nano_id(3) == "xxx"


def test_generate_nano_id_bson(monkeypatch):
    monkeypatch.setattr(nano_id, "generate_nano_id", lambda size=None: "a" * 24)

    bson_id = nano_id.generate_nano_id_bson()
    expected = hashlib.sha1(("a" * 24).encode()).hexdigest()[:24]

    assert isinstance(bson_id, ObjectId)
    assert str(bson_id) == expected
