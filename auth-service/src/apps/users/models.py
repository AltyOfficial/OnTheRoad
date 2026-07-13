from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.base.models import CreatedAtMixin, UpdatedAtMixin, UUIDMixin
from src.config.database.base import BaseOrmModel


class Role(CreatedAtMixin, UUIDMixin, BaseOrmModel):
    __tablename__ = "user_role"

    title: Mapped[str] = mapped_column(String(64))

    # relationships
    users: Mapped[List["User"]] = relationship(
        back_populates="role",
    )

    @property
    def get_display_value(self) -> str:
        return self.title

    def __str__(self):
        return self.get_display_value

class User(CreatedAtMixin, UpdatedAtMixin, UUIDMixin, BaseOrmModel):
    __tablename__ = "users"

    role_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("user_role.id", ondelete="SET NULL"),
    )

    login: Mapped[str] = mapped_column(
        String(128),
        unique=True,
    )
    hashed_password: Mapped[Optional[str]] = mapped_column(String(128))

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # relationships
    role: Mapped[Optional["Role"]] = relationship(
        back_populates="users",
    )
    sessions: Mapped[List["UserSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @property
    def get_display_value(self) -> str:
        return self.login
    
    def __str__(self):
        return self.get_display_value


class UserSession(CreatedAtMixin, UUIDMixin, BaseOrmModel):
    __tablename__ = "user_sessions"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    refresh_token_hash: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user_agent: Mapped[Optional[str]] = mapped_column(String(256))
    ip_address: Mapped[Optional[str]] = mapped_column(String(64))

    # relationships
    user: Mapped["User"] = relationship(
        back_populates="sessions",
    )

    @property
    def get_display_value(self) -> str:
        return f"Session for user {self.user_id} (expires at {self.expires_at})"

    def __str__(self):
        return self.get_display_value
