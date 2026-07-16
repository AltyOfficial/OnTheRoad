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
