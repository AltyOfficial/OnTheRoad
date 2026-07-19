from pydantic import PostgresDsn
from src.config.settings.base import CustomBaseSettings


class DatabaseConfig(CustomBaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    PG_SCHEME_ASYNC: str = "postgresql+asyncpg"
    PG_SCHEME_SYNC: str = "postgresql+psycopg2"

    PG_ECHO: bool = True

    def get_sqlalchemy_database_uri(self, scheme: str) -> str:
        return PostgresDsn.build(
            scheme=scheme,
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        ).unicode_string()
