# !/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
# Logger Configuration

This module provides centralized logging configuration for the FastAPI
application. It supports both console and file logging with customizable
formatters and handlers.
"""

import datetime
import logging.config
import os

import uvicorn

from src.core.env_config import get_settings


def init_logger(input_logger_name: str = None) -> logging.Logger:
    """
    Initialize the logger for the FastAPI application.

    NOTE: This function sets up the logging configuration for the
    application,  including console and file handlers. Ensure that the
    environment variables in `src/core/env_config.py` are properly
    configured before using this function.

    :param input_logger_name: The name of the logger to initialize. If not
        provided, the logger name is determined from the environment
        settings or defaults to 'application_logger'.
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
