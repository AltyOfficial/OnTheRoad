from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class DatabaseUnitOfWork(UnitOfWork):
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        pass 

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        if self.session.is_active:
            await self.session.rollback()

