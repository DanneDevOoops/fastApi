#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: skip-file

from types import SimpleNamespace

import pytest

from src.db.serializers.v2_serializers import v2_model_serializers as serializers

pytestmark = pytest.mark.unit


def test_individual_and_list_serializers():
    item = {
        "_id": "abc123",
        "name": "sensor",
        "description": "desc",
        "complete": False,
        "api_key": "token",
    }

    assert serializers.individual_serializer(item) == {
        "id": "abc123",
        "name": "sensor",
        "description": "desc",
        "complete": False,
        "api_key": "token",
    }
    assert serializers.list_serial([item]) == [serializers.individual_serializer(item)]


def test_model_serialize_and_user_list_serializer():
    model = SimpleNamespace(
        model_dump=lambda: {
            "_id": "user-1",
            "username": "alice",
            "email": "a@example.com",
        }
    )

    assert serializers.model_serialize(model) == {
        "id": "user-1",
        "username": "alice",
        "email": "a@example.com",
    }
    assert serializers.user_list_serializer([model]) == [
        serializers.model_serialize(model)
    ]
