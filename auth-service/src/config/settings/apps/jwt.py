from src.config.settings.base import CustomBaseSettings


class JWTConfig(CustomBaseSettings):
    JWT_SECRET_KEY: str
