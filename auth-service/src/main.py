import logging
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1.routes import routers as v1_routers
from src.config.logger import LOGGING
from src.config.settings import logger, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_sentry()
        yield
    except Exception as e:
        logger.error(f"Ошибка при запуске проекта: {str(e)}")
        raise e
    finally:
        logger.info("Завершение работы проекта")


def init_sentry():
    """Инициализация sentry."""

    if settings.sentry.SENTRY_KEY:
        sentry_sdk.init(
            dsn=settings.sentry.SENTRY_KEY,
            traces_sample_rate=0.01,
            auto_session_tracking=False,
        )


def create_app() -> FastAPI:
    """Создание приложения."""

    app = FastAPI(
        lifespan=lifespan,
        title=settings.app.PROJECT_NAME,
        version=settings.app.PROJECT_VERSION,
        description=settings.app.PROJECT_DESCRIPTION,
        default_response_class=ORJSONResponse,
        docs_url=settings.app.PROJECT_DOCS_URL,
        openapi_url=settings.app.PROJECT_OPENAPI_URL,
        redirect_slashes=False,
    )

    app.include_router(v1_routers)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
        root_path="/",
        forwarded_allow_ips="*",
        proxy_headers=True,
    )
