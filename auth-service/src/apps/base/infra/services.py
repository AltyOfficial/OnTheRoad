from abc import ABC, abstractmethod

from src.apps.base.infra.uow import UnitOfWork


class BaseService(ABC):
    @abstractmethod
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
