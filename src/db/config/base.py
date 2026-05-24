#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Base module for the database configuration.

This module contains the base class for the database configuration.

The following class is defined:

- Base: The declarative base class for SQLAlchemy.

Each class includes a detailed docstring with information about its purpose.

"""
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.utils.nano_id import generate_nano_id


class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Base database model."""

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=generate_nano_id,
    )
