from sqlalchemy import select

from src.apps.base.infra.repository import DatabaseRepository


class UserRepository(DatabaseRepository):
    
    async def get_by_login(self, login: str):
        """Get user by login."""

        stmt = select(self.model).where(self.model.login == login)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
