import hashlib
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.base.infra.security import get_security, Security
from src.apps.base.infra.services import BaseService
from src.apps.users.dto.user import UserBaseDTO, UserCreateDTO
from src.apps.users.exceptions import UserAlreadyExistsError
from src.apps.users.infra.uow import User, UserUnitOfWork
from src.config.database.sessions import get_async_session


class UserService(BaseService):
    def __init__(self, uow: UserUnitOfWork, security: Security):
        self.uow = uow
        self.security = security
    
    async def register(self, payload: UserCreateDTO) -> UserBaseDTO:
        """Register new User."""

        async with self.uow:
            existing_user = await self.uow.users.get_by_login(payload.login)
            if existing_user:
                raise UserAlreadyExistsError(f"User with login '{payload.login}' already exists.")
            
            hashed_password = self.security.hash_password(payload.password)

            user_data = {
                "login": payload.login,
                "hashed_password": hashed_password,
                "is_active": True,
                "is_verified": False,
            }
            new_user = await self.uow.users.create(user_data)

            await self.uow.commit()
        
        return UserBaseDTO.model_validate(new_user)

        

def get_user_service(
    session: AsyncSession = Depends(get_async_session),
    security: Security = Depends(get_security)
) -> UserService:
    """Dependency injection for UserService."""

    uow = UserUnitOfWork(session=session)

    return UserService(uow=uow, security=security)
