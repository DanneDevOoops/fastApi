#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This module contains the configuration settings for the FastAPI application.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Class to define the configuration settings for the application.
    """

    # --- Environment -------------------------------------------------------
    env_name: str = Field(
        default="development",
        json_schema_extra={"env_name": "ENV_NAME"})
    pyenv_version: str = Field(
        default="3.11.4",
        json_schema_extra={"env_name": "PYENV_VERSION"})
    app_debug: bool = Field(
        default=False,
        json_schema_extra={"env_name": "APP_DEBUG"})

    # --- Application -------------------------------------------------------
    app_name: str = Field(
        default="Fast API application",
        json_schema_extra={"env_name": "APP_NAME"})
    app_host: str = Field(
        default="localhost",
        json_schema_extra={"env_name": "APP_HOST"})
    app_port: int = Field(
        default=1337,
        json_schema_extra={"env_name": "APP_PORT"})
    app_reload: bool = Field(
        default=True,
        json_schema_extra={"env_name": "APP_RELOAD"})
    app_logger_name: str = Field(
        default="application_logger",
        json_schema_extra={"env_name": "LOGGER_NAME"})

    # --- Secret Keys (JWT) --------------------------------------------------
    app_algorithm: str = Field(
        default="HS256",
        json_schema_extra={"env_name": "APP_ALGORITHM"})
    app_jwt_secret_key: str = Field(
        default="a_secret_key",
        json_schema_extra={"env_name": "APP_JWT_SECRET_KEY"})

    # --- Applications registered with the API -------------------------------
    app_health_check_api_key: str = Field(
        default=None,
        json_schema_extra={"env_name": "APP_HEALTH_CHECK_API_KEY"})
    app_1_api_key: str = Field(
        default=None,
        json_schema_extra={"env_name": "APP_1_API_KEY"})

    # app_2_api_key: str = Field(
    #     default=None,
    #     json_schema_extra={"env_name": "APP_1_API_KEY"})

    # --- Console Logger settings --------------------------------------------
    console_logger_level: str = Field(
        default="DEBUG",
        json_schema_extra={"env_name": "CONSOLE_LOGGER_LEVEL"})
    console_logger_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        json_schema_extra={"env_name": "CONSOLE_LOGGER_FORMAT"})
    console_logger_propagate: bool = Field(
        default=False,
        json_schema_extra={"env_name": "CONSOLE_LOGGER_PROPAGATE"})

    # --- File Logger settings -----------------------------------------------
    file_logger_level: str = Field(
        default="DEBUG",
        json_schema_extra={"env_name": "FILE_LOGGER_LEVEL"})
    file_logger_file_name: str = Field(
        default="fastapi_log",
        json_schema_extra={"env_name": "FILE_LOGGER_FILE_NAME"})
    file_logger_file_size: int = Field(
        default=1000000,
        json_schema_extra={"env_name": "FILE_LOGGER_FILE_SIZE"})
    file_logger_file_count: int = Field(
        default=3,
        json_schema_extra={"env_name": "FILE_LOGGER_FILE_COUNT"})
    file_logger_dir: str = Field(
        default="./../logs",
        json_schema_extra={"env_name": "FILE_LOGGER_DIR"})
    file_logger_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        json_schema_extra={"env_name": "FILE_LOGGER_FORMAT"})
    file_logger_mode: str = Field(
        default="w",
        json_schema_extra={"env_name": "FILE_LOGGER_MODE"})
    file_logger_propagate: bool = Field(
        default=False,
        json_schema_extra={"env_name": "FILE_LOGGER_PROPAGATE"})
    file_logger_docker_host_machine_path: str = Field(
        default="/var/log/fastapi",
        json_schema_extra={"env_name": "FILE_LOGGER_DOCKER_HOST_MACHINE_PATH"})

    # --- Postgres Database --------------------------------------------------
    pg_db_url: str = Field(
        default="postgresql://"
                "a_postgresql_db_username:"
                "a_postgresql_db_password@"
                "the_db_host:"
                "5432/the_db_name",
        json_schema_extra={"env_name": "PG_DB_URL"})
    pg_db_name: str = Field(
        default="the_db_name",
        json_schema_extra={"env_name": "PG_DB_NAME"})
    pg_db_host: str = Field(
        default="the_db_host",
        json_schema_extra={"env_name": "PG_DB_HOST"})
    pg_db_port: int = Field(
        default=5432,
        json_schema_extra={"env_name": "PG_DB_PORT"})
    pg_db_username: str = Field(
        default="a_postgresql_db_username",
        json_schema_extra={"env_name": "PG_DB_USERNAME"})
    pg_db_password: str = Field(
        default="a_postgresql_db_password",
        json_schema_extra={"env_name": "PG_DB_PASSWORD"})
    pg_db_backup_dir: str = Field(
        default="./src/db/db_scripts", json_schema_extra={
            "env_name": "PG_DB_BACKUP_DIR"})
    pg_db_docker_host_machine_backup_path: str = Field(
        default="~/documents/db/backup",
        json_schema_extra={
            "env_name": "PG_DB_DOCKER_HOST_MACHINE_BACKUP_PATH"})
    pg_db_connection_pool_size: int = Field(
        default=100,
        json_schema_extra={"env_name": "PG_DB_CONNECTION_POOL_SIZE"})
    pg_db_max_overflow: int = Field(
        default=0,
        json_schema_extra={"env_name": "PG_DB_MAX_OVERFLOW"})
    pg_db_echo: bool = Field(
        default=False,
        json_schema_extra={"env_name": "PG_DB_ECHO"})
    pg_db_future: bool = Field(
        default=True,
        json_schema_extra={"env_name": "PG_DB_FUTURE"})
    pg_db_auto_commit: bool = Field(
        default=False,
        json_schema_extra={"env_name": "PG_DB_AUTO_COMMIT"})
    pg_db_auto_flush: bool = Field(
        default=False,
        json_schema_extra={"env_name": "PG_DB_AUTO_FLUSH"})
    pg_db_pre_ping: bool = Field(
        default=True,
        json_schema_extra={"env_name": "PG_DB_PRE_PING"})
    pg_db_expire_on_commit: bool = Field(
        default=False,
        json_schema_extra={"env_name": "PG_DB_EXPIRE_ON_COMMIT"})
    pg_db_volume_path: str = Field(
        default="/var/lib/postgresql/data",
        json_schema_extra={"env_name": "PG_DB_VOLUME_PATH"})
    pg_local_user_id: int = Field(
        default=1000,
        json_schema_extra={"env_name": "PG_LOCAL_USER_ID"})
    pg_local_group_id: int = Field(
        default=1000,
        json_schema_extra={"env_name": "PG_LOCAL_GROUP_ID"})
    pg_db_docker_service_name: str = Field(
        default="the_db_docker_service_name",
        json_schema_extra={"env_name": "PG_DB_DOCKER_SERVICE_NAME"})
    pg_db_docker_data_path: str = Field(
        default="/var/lib/postgresql/data",
        json_schema_extra={"env_name": "PG_DB_DOCKER_DATA_PATH"})

    # --- MongoDB Database ---------------------------------------------------
    mongo_db_url: str = Field(
        default="mongodb://a_mongodb_db_username:"
                "a_mongodb_db_password@"
                "the_db_host:"
                "27017",
        json_schema_extra={"env_name": "MONGO_DB_URL"})
    mongo_db_name: str = Field(
        default="the_mongo_db_name",
        json_schema_extra={"env_name": "MONGO_DB_NAME"})
    mongo_db_host: str = Field(
        default="the_mongo_db_host",
        json_schema_extra={"env_name": "MONGO_DB_HOST"})
    mongo_db_port: int = Field(
        default=27017,
        json_schema_extra={"env_name": "MONGO_DB_PORT"})
    mongo_db_username: str = Field(
        default="a_mongodb_db_username",
        json_schema_extra={"env_name": "MONGO_DB_USERNAME"})
    mongo_db_password: str = Field(
        default="a_mongodb_db_password",
        json_schema_extra={"env_name": "MONGO_DB_PASSWORD"})

    # SQLite3 Database settings
    sqlite_db_url: str = Field(
        default="sqlite:///a_sqlite_db_name.db",
        json_schema_extra={"env_name": "SQLITE_DB_URL"})

    # Pydantic config of .env file
    model_config = SettingsConfigDict(env_file=".env")

    def __str__(self) -> str:
        """
        Method to return the string representation of the class.
        """
        return str(self.__dict__)


@lru_cache
def get_settings() -> Settings:
    """
    Function to get the settings.
    """
    return Settings()
