from datetime import datetime
from typing import Optional
from uuid import UUID

from src.api.v1.base.schemas import CustomBaseModel


class UserDetailResponseSchema(CustomBaseModel):
    id: UUID
    role_id: Optional[UUID]
    login: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateRequestSchema(CustomBaseModel):
    login: str
    password: str


class UserLoginRequestSchema(CustomBaseModel):
    login: str
    password: str


class AuthTokenResponseSchema(CustomBaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
