from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config.settings import settings

async_engine = create_async_engine(
    settings.db.get_sqlalchemy_database_uri(settings.db.PG_SCHEME_ASYNC),
    echo=settings.db.PG_ECHO,
    future=True,
)

sync_engine = create_engine(
    settings.db.get_sqlalchemy_database_uri(settings.db.PG_SCHEME_SYNC),
)

sync_session = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
)

async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
