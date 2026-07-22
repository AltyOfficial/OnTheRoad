from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text, UUID, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.base.models import CreatedAtMixin, DisplayMixin, IsPublishedMixin, UpdatedAtMixin, UUIDMixin
from src.config.database.base import BaseOrmModel

if TYPE_CHECKING:
    from src.apps.profiles.models import Profile


class Tag(UUIDMixin, CreatedAtMixin, DisplayMixin, BaseOrmModel):
    __tablename__ = 'tag'

    title: Mapped[str] = mapped_column(String(128))
    slug: Mapped[str] = mapped_column(String(128), unique=True)

    # relationships
    posts: Mapped[List["PostTag"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan",
    )



class Country(UUIDMixin, CreatedAtMixin, DisplayMixin, BaseOrmModel):
    __tablename__ = 'country'
    
    title: Mapped[str] = mapped_column(String(128))
    slug: Mapped[str] = mapped_column(String(128), unique=True)

    # relationships
    posts: Mapped[List["PostCountry"]] = relationship(
        back_populates="country",
        cascade="all, delete-orphan",
    )


class Post(UUIDMixin, CreatedAtMixin, UpdatedAtMixin, DisplayMixin, BaseOrmModel):
    __tablename__ = 'post'

    title: Mapped[str] = mapped_column(String(256))
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    cover_image_url: Mapped[Optional[str]] = mapped_column(String(512))

    author_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("profile.id", ondelete="SET NULL"),
    )

    blocks: Mapped[list] = mapped_column(JSONB, default=list)

    route_type: Mapped[str] = mapped_column(String(32), default="hybrid")
    status: Mapped[str] = mapped_column(String(32), default="published")

    duration: Mapped[Optional[str]] = mapped_column(String(64))
    read_time: Mapped[int]

    like_count: Mapped[int]
    view_count: Mapped[int]

    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # relationships
    author: Mapped[Optional["Profile"]] = relationship(
        back_populates="posts",
    )
    tags: Mapped[List["PostTag"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
    )
    countries: Mapped[List["PostCountry"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
    )


# M2M RELATIONSHIPS
class PostTag(UUIDMixin, DisplayMixin, BaseOrmModel):
    __tablename__ = "post_tag"
    __table_args__ = (
        UniqueConstraint(
            "post_id",
            "tag_id",
            name="post_tag_uix",
        ),
    )

    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"),
    )
    tag_id: Mapped[UUID] = mapped_column(
        ForeignKey("tag.id", ondelete="RESTRICT"),
    )

    # relationships
    post: Mapped["Post"] = relationship(
        back_populates="tags",
    )
    tag: Mapped["Tag"] = relationship(
        back_populates="posts",
    )

    @property
    def get_display_value(self) -> str:
        return f"{self.post.get_display_value} - {self.tag.get_display_value}"


class PostCountry(UUIDMixin, DisplayMixin, BaseOrmModel):
    __tablename__ = "post_country"
    __table_args__ = (
        UniqueConstraint(
            "post_id",
            "country_id",
            name="post_country_uix",
        ),
    )

    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"),
    )
    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("country.id", ondelete="RESTRICT"),
    )

    # relationships
    post: Mapped["Post"] = relationship(
        back_populates="countries",
    )
    country: Mapped["Country"] = relationship(
        back_populates="posts",
    )

    @property
    def get_display_value(self) -> str:
        return f"{self.post.get_display_value} - {self.country.get_display_value}"
