import os
from typing import Optional

import pydantic

ENV_FILE = os.getenv("ENV_FILE", ".env")


class BaseSettings(pydantic.BaseSettings):
    """Base class for loading settings.
    The setting variables are loaded from environment settings first, then from the defined env_file.

    Different groups/contexts of settings are created using different classes, that can define an env_prefix which
    will be concatenated to the start of the variable name."""

    class Config:
        env_file = ENV_FILE


class APISettings(BaseSettings):
    """Settings related with the FastAPI server"""

    host: str = "0.0.0.0"
    port: int = 8000

    class Config(BaseSettings.Config):
        env_prefix = "API_"


class APIDocsSettings(BaseSettings):
    """Settings related with the API autogenerated documentation"""

    title: str = "restaurant_menu_bot"
    """Title of the API"""
    description: Optional[str] = None
    """Description of the API"""
    version: str = "version"
    """Version of the API"""

    class Config(BaseSettings.Config):
        env_prefix = "API_DOCS_"


class RequestLoggingSettings(BaseSettings):
    """Settings related with the logging of requests"""

    level: str = "DEBUG"
    serialize: bool = False

    class Config(BaseSettings.Config):
        env_prefix = "REQUEST_LOG_"


api_settings = APISettings()
api_docs_settings = APIDocsSettings()
request_logging_settings = RequestLoggingSettings()