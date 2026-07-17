from typing import Optional
from uuid import UUID
from datetime import datetime

from src.apps.base.dto.base import BaseDTO


class UserBaseDTO(BaseDTO):
    id: UUID
    role_id: Optional[UUID]
    login: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateDTO(BaseDTO):
    login: str
    password: str


class UserLoginDTO(BaseDTO):
    login: str
    password: str


class AuthTokensDTO(BaseDTO):
    """JWT tokens DTO."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime
