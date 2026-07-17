import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.base.infra.security import get_security, Security
from src.apps.base.infra.services import BaseService
from src.apps.users.dto.user import AuthTokensDTO, UserBaseDTO, UserCreateDTO, UserLoginDTO
from src.apps.users.exceptions import InvalidCredentialsError, UserAlreadyExistsError
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
            new_user = await self.uow.users.create(data = user_data)

            await self.uow.commit()
        
        return UserBaseDTO.model_validate(new_user)
    
    async def login(
        self,
        payload: UserLoginDTO,
        user_agent: Optional[str],
        ip_address: Optional[str],
    ) -> AuthTokensDTO:
        """Authenticate user and return jwt tokens."""

        async with self.uow:
            user = await self.uow.users.get_by_login(payload.login)
            if not user or not self.security.verify_password(payload.password, user.hashed_password):
                raise InvalidCredentialsError("Invalid login credentials.")
            
            await self.uow.user_sessions.delete_expired_sessions(user_id=user.id)
            await self.uow.user_sessions.keep_last_sessions(user_id=user.id, max_sessions=5)
            
            access_token = self.security.create_access_token(user_id=user.id)
            refresh_token, expire = self.security.create_refresh_token(user_id=user.id)

            token_hash = self.security.hash_token_sha256(refresh_token)

            user_session_data = {
                "user_id": user.id,
                "refresh_token_hash": token_hash,
                "expires_at": expire,
                "user_agent": user_agent,
                "ip_address": ip_address
            }
            await self.uow.user_sessions.create(data=user_session_data)

            await self.uow.commit()
        
        return AuthTokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_at=expire,
        )
        

def get_user_service(
    session: AsyncSession = Depends(get_async_session),
    security: Security = Depends(get_security)
) -> UserService:
    """Dependency injection for UserService."""

    uow = UserUnitOfWork(session=session)

    return UserService(uow=uow, security=security)
