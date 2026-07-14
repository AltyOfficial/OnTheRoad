from fastapi import Depends
from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.base.infra.uow import DatabaseUnitOfWork


class UserUnitOfWork(DatabaseUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
