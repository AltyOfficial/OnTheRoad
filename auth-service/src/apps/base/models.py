from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
    )


class IsPublishedMixin:
    is_published: Mapped[bool] = mapped_column(default=True)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )
