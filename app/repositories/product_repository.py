from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def get_by_id_with_category(self, id: int) -> Product | None:
        result = await self.session.execute(
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == id, Product.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def get_all_with_category(self, offset: int = 0, limit: int = 100) -> list[Product]:
        result = await self.session.execute(
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.is_deleted.is_(False))
            .order_by(Product.name)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Product | None:
        result = await self.session.execute(
            select(Product).where(Product.id == id, Product.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Product]:
        result = await self.session.execute(
            select(Product)
            .where(Product.is_deleted.is_(False))
            .order_by(Product.name)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
