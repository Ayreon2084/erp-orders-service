"""Order and order-products repository."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.order import Order, OrderProduct
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    async def get_by_id_with_items(self, id: int) -> Order | None:
        result = await self.session.execute(
            select(Order)
            .options(
                selectinload(Order.order_products).selectinload(OrderProduct.product)
            )
            .where(Order.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all_with_items(self, offset: int = 0, limit: int = 100) -> list[Order]:
        result = await self.session.execute(
            select(Order)
            .options(
                selectinload(Order.order_products).selectinload(OrderProduct.product),
                selectinload(Order.client)
            )
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Order | None:
        result = await self.session.execute(
            select(Order).where(Order.id == id)
        )
        return result.scalar_one_or_none()

    async def get_order_product(
        self, order_id: int, product_id: int
    ) -> OrderProduct | None:
        result = await self.session.execute(
            select(OrderProduct).where(
                OrderProduct.order_id == order_id,
                OrderProduct.product_id == product_id
            )
        )
        return result.scalar_one_or_none()
