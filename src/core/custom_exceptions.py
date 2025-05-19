#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Custom Exceptions module.

This module defines custom exception classes used throughout the application.
Each exception class inherits from the base `Exception` class and includes
additional attributes and methods to provide more context and functionality.
"""
import logging

from src.core.env_config import get_settings

settings = get_settings()
logger = logging.getLogger(
    settings.app_logger_name or "application_logger")


class BaseCustomException(Exception):
    """
    Base class for custom exceptions.

    Attributes
    ----------
    .. attribute:: message
       :type: str

       The error message describing the error.

    .. attribute:: status_code
       :type: int

       The HTTP status code for the error.

    .. attribute:: type
       :type: str

       The type of error.
    """

    def __init__(self, message: str, status_code: int, error_type: str):
        """
        Constructor for the BaseCustomException class.

        :param message: The error message describing the error.
        :type message: str
        :param status_code: The HTTP status code for the error.
        :type status_code: int
        :param error_type: The type of error.
        :type error_type: str

        :return: None
        """
        super().__init__(message)
        self.status_code = status_code
        self.type = error_type

    def __str__(self) -> str:
        """
        String representation of the BaseCustomException.

        Returns
        -------
        :return: A string representation of the BaseCustomException
        :rtype: str
        """
        return f"{self.type}: {self.args[0]}"


class AuthException(BaseCustomException):
    """
    Exception raised for errors in the authentication process.
    """

    def __init__(self, message: str):
        self.detail = message
        super().__init__(
            message, 401, 'UnauthorizedException')


class BadRequestException(BaseCustomException):
    """
    Exception raised for errors in the request body.
    """

    def __init__(self, message: str):
        self.detail = message
        super().__init__(
            message, 400, 'BadRequestException')


class ConflictException(BaseCustomException):
    """
    Exception raised for errors when a resource is in conflict.
    """

    def __init__(self, message: str):
        self.detail = message
        super().__init__(
            message, 409, 'ConflictException')


class DatabaseException(BaseCustomException):
    """
    Exception raised for errors when a database error occurs.
    """

    def __init__(self, message: str):
        self.detail = message
        super().__init__(
            message, 500, 'DatabaseException')


class HTTPException(BaseCustomException):
    """
    Exception raised for errors when an HTTP error occurs.
    """

    def __init__(self, message: str):
        self.detail = message
        super().__init__(
            message, 500, 'HTTPException')


class InternalServerException(BaseCustomException):
    """
    Exception raised for errors when an internal server error occurs.
    """

    def __init__(self, message: str):
        self.detail = message
        super().__init__(
            message, 500, 'InternalServerException')


class NotFoundException(BaseCustomException):
    """
    Exception raised for errors when a resource is not found.
    """

    def __init__(self, message: str):
        self.detail = message
        super().__init__(
            message, 404, 'NotFoundException')


class ValidationException(BaseCustomException):
    """
    Exception raised for errors when a validation error occurs.
    """

    def __init__(self, message: str):
        self.detail = message
        super().__init__(
            message, 422, 'ValidationException')
