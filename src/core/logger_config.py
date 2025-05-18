# !/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Logger Configuration Module
===========================

This module contains the logger configuration for the FastAPI application.

.. note::
    The module is responsible for setting up and configuring the logging system
    used by the application. It supports both console and file logging, with customizable
    formatters and handlers. Ensure that the environment variables in `src/core/env_config.py`
    are properly configured to use this module effectively.

Functions
---------
- :func:`init_logger`: Initializes and returns a configured logger instance.

Dependencies
------------
- `datetime`: Used for generating timestamps for log files.
- `logging.config`: Provides the ability to configure logging using a dictionary.
- `os`: Used for file and directory operations.
- `uvicorn`: Provides default logging formatters for Uvicorn.
- `src.core.env_config`: Supplies application settings via the `get_settings` function.

Environment Variables
---------------------
- `app_logger_name`: Name of the logger.
- `file_logger_dir`: Directory where log files are stored.
- `file_logger_file_name`: Name of the log file.
- `console_logger_level`: Logging level for the console logger.
- `file_logger_level`: Logging level for the file logger.
- `file_logger_mode`: File mode for the log file (e.g., 'w' for overwrite).

Usage
-----
1. Import the :func:`init_logger` function.
2. Call the function to initialize the logger.
3. Use the returned logger instance for logging messages.

Example
-------
.. code-block:: python

    from src.core.logger_config import init_logger

    logger = init_logger()
    logger.info("Application started successfully.")
"""

import datetime
import logging.config
import os

import uvicorn

from src.core.env_config import get_settings


def init_logger(input_logger_name: str = None) -> logging.Logger:
    """
    Initialize the logger for the FastAPI application.

    NOTE: This function sets up the logging configuration for the application, including
    console and file handlers. Ensure that the environment variables in `src/core/env_config.py`
    are properly configured before using this function.

    :param input_logger_name: The name of the logger to initialize. If not provided, the logger
                              name is determined from the environment settings or defaults to
                              'application_logger'.
    :type input_logger_name: str, optional
    :return: A configured logger instance.
    :rtype: logging.Logger
    :raises OSError: If the log directory cannot be created.
    """

    # Initialize settings from environment configuration
    settings = get_settings()
    logger_name = (settings.app_logger_name or input_logger_name
                   or 'application_logger')

    # Define the logging configuration dictionary
    log_dir = settings.file_logger_dir or 'logs'
    startup_time = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    file_name = str(startup_time + "_" + settings.file_logger_file_name or
                    'application.log')
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, file_name)

    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'uvicorn_console': {
                '()': uvicorn.logging.DefaultFormatter,
                'fmt': '%(levelprefix)s %(asctime)s | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'uvicorn_access': {
                '()': uvicorn.logging.AccessFormatter,
                'fmt': '%(levelprefix)s %(asctime)s | %(client_addr)s - '
                       '"%(request_line)s" %(status_code)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'default': {
                'format': '%(asctime)s - %(name)s - '
                          '%(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            }
        },
        'handlers': {
            'console_logger_handler': {
                'class': 'logging.StreamHandler',
                'level': settings.console_logger_level or 'DEBUG',
                'formatter': 'uvicorn_console',
                'stream': 'ext://sys.stdout',
            },
            'file_logger_handler': {
                'class': 'logging.FileHandler',
                'level': settings.file_logger_level or 'INFO',
                'formatter': 'default',
                'filename': log_file_path,
                'mode': settings.file_logger_mode or 'w',
            }
        },
        'loggers': {
            logger_name: {
                'level': settings.console_logger_level or 'DEBUG',
                'handlers': ['console_logger_handler', 'file_logger_handler'],
                'propagate': False,
            }
        },
    }

    # Apply the logging configuration
    logging.config.dictConfig(log_config)

    # Get the loggers
    logger = logging.getLogger(logger_name)

    return logger
