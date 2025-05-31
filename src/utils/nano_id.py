#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Utility functions for generating unique Nano IDs and BSON ObjectIds.

This module provides functions to generate customizable Nano IDs using the
`nanoid` library, with support for environment-based configuration of
character set and size. It also includes a function to create BSON
ObjectIds derived from Nano IDs, suitable for use as unique identifiers in
MongoDB and other systems.

Environment Variables:
- `NANO_ID_CHARACTERS`: Characters to use for Nano ID generation (default:
    alphanumeric).
- `NANO_ID_SIZE`: Length of the Nano ID (default: 24).

Functions:
- generate_nano_id: Generate a unique Nano ID with optional size.
- generate_nano_id_bson: Generate a BSON ObjectId based on a Nano ID.
"""

import hashlib
import os

from bson import ObjectId
from nanoid import generate


def generate_nano_id(size: int | None = None) -> str:
    """
    Generate a unique Nano ID.

    Generates a Nano ID using the `nanoid` library. The characters and size
    of the Nano ID can be customized using the `NANO_ID_CHARACTERS` and
    `NANO_ID_SIZE` environment variables, or by passing the `size` argument.

    :param size: Optional. The length of the Nano ID to generate. If not
        provided, uses the `NANO_ID_SIZE` environment variable or defaults
        to 24.
    :type size: int or None
    :return: A unique Nano ID string.
    :rtype: str
    """
    id_characters: str = os.getenv(
        'NANO_ID_CHARACTERS',
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    )

    if not size:
        # Default size is 25 if not specified in the environment variable
        id_size: int = int(os.getenv('NANO_ID_SIZE', '24'))
    else:
        id_size: int = size
    new_nano_id: str = generate(id_characters, int(id_size))

    return new_nano_id


def generate_nano_id_bson() -> ObjectId:
    """
    Generate a BSON ObjectId from a Nano ID.

    Creates a Nano ID of length 24, hashes it using SHA-1, and returns a
    BSON ObjectId from the first 24 hex characters of the hash.

    :return: A BSON ObjectId derived from a Nano ID.
    :rtype: ObjectId
    """
    nano_id = generate_nano_id(24)
    hex_str = hashlib.sha1(nano_id.encode()).hexdigest()[:24]
    return ObjectId(hex_str)
