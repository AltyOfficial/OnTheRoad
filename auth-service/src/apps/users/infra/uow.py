from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.base.infra.uow import DatabaseUnitOfWork
from src.apps.users.models import User, Role, UserSession
from src.apps.users.infra.repositories.role import RoleRepository
from src.apps.users.infra.repositories.user import UserRepository
from src.apps.users.infra.repositories.user_session import UserSessionRepository


class UserUnitOfWork(DatabaseUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self._user_repository = UserRepository(model=User, db_session=session)
        self._user_role_repository = RoleRepository(model=Role, db_session=session)
        self._user_session_repository = UserSessionRepository(model=UserSession, db_session=session)
    
    @property
    def roles(self) -> RoleRepository:
        return self._user_role_repository

    @property
    def users(self) -> UserRepository:
        return self._user_repository
    
    @property
    def user_sessions(self) -> UserSessionRepository:
        return self._user_session_repository
