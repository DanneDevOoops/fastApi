#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
User model for the database
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import Mapped

from src.db.config.base import Base


class User(Base):
    """
    User model for the database
    """

    __tablename__ = "users"

    id: Mapped[str] = Column(String, primary_key=True, index=True)
    username: Mapped[str] = Column(String, unique=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    password: Mapped[str] = Column(String)

    # User details
    first_name: Mapped[str] = Column(String)
    last_name: Mapped[str] = Column(String)
    phone_number: Mapped[str] = Column(String)
    address: Mapped[str] = Column(String)
    city: Mapped[str] = Column(String)
    state: Mapped[str] = Column(String)
    country: Mapped[str] = Column(String)
    zip_code: Mapped[str] = Column(String)

    # User roles
    is_active: Mapped[bool] = Column(Boolean, default=True)
    is_superuser: Mapped[bool] = Column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    deleted_at: Mapped[datetime] = Column(DateTime, default=None)

    def __dir__(self) -> list:
        """
        Return the list of columns in the table

        :return: The list of columns in the table
        :rtype: list
        """
        return self.__table__.columns.keys()

    def __str__(self) -> str:
        """
        Return the string representation of the model

        :return: The string representation of the model
        :rtype: str
        """
        return (
            f"UserModel(id={self.id}, username={self.username}, email" f"={self.email})"
        )

    def __eq__(self, other) -> bool:
        """
        Check if two UserModel instances are equal

        :param other: The other UserModel instance to compare with
        :type other: User
        :return: True if the two instances are equal, False otherwise
        :rtype: bool
        """
        if isinstance(other, User):
            return self.id == other.id
        return False
