from src.config.settings.base import CustomBaseSettings


class SentryConfig(CustomBaseSettings):
    SENTRY_KEY: str
    SENTRY_ENVIRONMENT: str = "development"
