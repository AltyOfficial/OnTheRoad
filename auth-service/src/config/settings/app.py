from src.config.settings.base import CustomBaseSettings


class AppConfig(CustomBaseSettings):
    PROJECT_NAME: str
    PROJECT_V1_URL: str = "/api/v1"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "auth API"
    PROJECT_DOCS_URL: str = "/api/docs/"
    PROJECT_OPENAPI_URL: str = "/api/openapi.json"
