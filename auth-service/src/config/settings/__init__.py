import logging

from pydantic import BaseModel

from src.config.settings.app import AppConfig
from src.config.settings.apps.sentry import SentryConfig


class MainConfig(BaseModel):
    TESTING_MODE: bool = False
    app: AppConfig = AppConfig()
    sentry: SentryConfig = SentryConfig()


logger = logging.getLogger("auth-logger")
settings = MainConfig()
