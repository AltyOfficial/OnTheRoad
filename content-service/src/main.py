import logging
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.config.logger import LOGGING
from src.config.settings import logger, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_sentry()
        yield
    except Exception as e:
        logger.error(f"Error starting the app: {str(e)}")
        raise e
    finally:
        logger.info("Exiting")


def init_sentry():
    if settings.sentry.SENTRY_KEY:
        sentry_sdk.init(
            dsn=settings.sentry.SENTRY_KEY,
            traces_sample_rate=0.01,
            auto_session_tracking=False,
        )


def create_app() -> FastAPI:
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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

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
