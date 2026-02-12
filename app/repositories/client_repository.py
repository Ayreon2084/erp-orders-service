from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.repositories.base import BaseRepository


class ClientRepository(BaseRepository[Client]):
    def __init__(self, session: AsyncSession):
        super().__init__(Client, session)

    async def get_by_email(self, email: str) -> Client | None:
        result = await self.session.execute(
            select(Client).where(Client.email == email, Client.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Client | None:
        result = await self.session.execute(
            select(Client).where(Client.id == id, Client.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Client]:
        result = await self.session.execute(
            select(Client)
            .where(Client.is_deleted.is_(False))
            .order_by(Client.full_name)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
