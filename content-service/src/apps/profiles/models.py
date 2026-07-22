from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text, UUID, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.base.models import CreatedAtMixin, DisplayMixin, IsPublishedMixin, UpdatedAtMixin, UUIDMixin
from src.config.database.base import BaseOrmModel

if TYPE_CHECKING:
    from src.apps.posts.models import Post


class Profile(CreatedAtMixin, UpdatedAtMixin, UUIDMixin, BaseOrmModel):
    __tablename__ = "profile"

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True)

    username: Mapped[str] = mapped_column(String(64), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(64))
    last_name: Mapped[Optional[str]] = mapped_column(String(64))

    # relationships
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
    )

    @property
    def get_display_value(self) -> str:
        return self.username
