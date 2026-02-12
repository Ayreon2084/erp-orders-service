from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import OrderStatus
from app.db.models.order import Order, OrderProduct
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.client_repository import ClientRepository
from app.schemas.order import OrderProductAdd


class OrderService:
    def __init__(self, session: AsyncSession):
        self.repository = OrderRepository(session)
        self.product_repository = ProductRepository(session)
        self.client_repository = ClientRepository(session)
        self.session = session

    async def create_order(self, client_id: int) -> Order:
        client = await self.client_repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        new_order = Order(client_id=client_id, status=OrderStatus.NEW)
        await self.repository.create(new_order)
        return await self.repository.get_by_id_with_items(new_order.id)

    async def get_order(self, order_id: int) -> Order:
        order = await self.repository.get_by_id_with_items(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return order

    async def get_orders(self, offset: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_all_with_items(offset, limit)

    async def add_item_to_order(
        self, order_id: int, item_data: OrderProductAdd
    ) -> Order:
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        product = await self.product_repository.get_by_id(item_data.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if product.quantity < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock. Available: {product.quantity}"
            )

        existing_item = await self.repository.get_order_product(
            order_id, item_data.product_id
        )

        if existing_item:
            existing_item.quantity += item_data.quantity
        else:
            new_item = OrderProduct(
                order_id=order_id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                price_at_order=product.price
            )
            self.session.add(new_item)

        product.quantity -= item_data.quantity
        await self.session.commit()
        return await self.repository.get_by_id_with_items(order_id)

    async def add_items_to_order(
        self, order_id: int, items: list[OrderProductAdd]
    ) -> Order:
        """Add multiple items to an order in one request. Same merge/stock rules as add_item_to_order."""
        for item in items:
            await self.add_item_to_order(order_id, item)
        return await self.repository.get_by_id_with_items(order_id)

    async def update_order_status(
        self, order_id: int, new_status: OrderStatus
    ) -> Order:
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        order.status = new_status
        await self.repository.update(order)
        return await self.repository.get_by_id_with_items(order_id)

    async def delete_order(self, order_id: int) -> None:
        order = await self.repository.get_by_id_with_items(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        for order_product in order.order_products:
            product = await self.product_repository.get_by_id(order_product.product_id)
            if product:
                product.quantity += order_product.quantity

        await self.session.delete(order)
        await self.session.commit()
