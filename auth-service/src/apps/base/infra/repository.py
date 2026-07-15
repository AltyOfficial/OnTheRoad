from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar, Optional, Sequence
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database.base import BaseOrmModel


class AbstractRepository(ABC):

    @abstractmethod
    async def get_by_id(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=BaseOrmModel)


class DatabaseRepository(AbstractRepository, Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: UUID) -> Optional[ModelType]:

        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[ModelType]:
        
        stmt = select(self.model)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def create(self, data: dict) -> ModelType:

        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()

        return instance

    async def update(self, data: dict, **filters: Any) -> ModelType:

        stmt = update(self.model).filter_by(**filters).values(**data).returning(self.model)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete(self, **filters: Any) -> None:
        """Удаление записи в базе данных."""

        await self.session.execute(delete(self.model).filter_by(**filters))

