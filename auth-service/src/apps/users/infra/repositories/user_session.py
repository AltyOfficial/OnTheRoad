from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select

from src.apps.base.infra.repository import DatabaseRepository


class UserSessionRepository(DatabaseRepository):
    
    async def delete_expired_sessions(self, user_id: UUID) -> None:
        """Delete expired sessions for a user."""
        
        stmt = delete(self.model).where(
            self.model.user_id == user_id,
            self.model.expires_at < datetime.utcnow()
        )
        await self.session.execute(stmt)

    async def keep_last_sessions(self, user_id: UUID, max_sessions: int) -> None:
        """Keep only the last `max_sessions` sessions for a user."""

        subq = (
            select(self.model.id)
            .where(self.model.user_id == user_id)
            .order_by(self.model.expires_at.desc())
            .limit(max_sessions)
            .subquery()
        )
        delete_stmt = delete(self.model).where(
            self.model.user_id == user_id,
            self.model.id.not_in(select(subq))
        )
        await self.session.execute(delete_stmt)
