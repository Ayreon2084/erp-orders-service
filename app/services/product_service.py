"""Product business logic: CRUD, SKU generation and soft delete."""
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Product CRUD; validates category and generates SKU when omitted."""

    def __init__(self, session: AsyncSession):
        self.repository = ProductRepository(session)
        self.category_repository = CategoryRepository(session)
        self.session = session

    async def create_product(self, data: ProductCreate) -> Product:
        category = await self.category_repository.get_by_id(data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        product_dict = data.model_dump()
        if not product_dict.get("sku"):
            prefix = product_dict["name"][:3].upper()
            suffix = str(uuid4()).split("-")[0].upper()
            product_dict["sku"] = f"{prefix}-{suffix}"

        new_product = Product(**product_dict)
        try:
            await self.repository.create(new_product)
            await self.session.commit()
            return new_product
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists"
            )

    async def get_product(self, product_id: int) -> Product:
        product = await self.repository.get_by_id_with_category(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product

    async def get_products(self, offset: int = 0, limit: int = 100) -> list[Product]:
        return await self.repository.get_all_with_category(offset, limit)

    async def update_product(
        self, product_id: int, data: ProductUpdate
    ) -> Product:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if data.category_id and data.category_id != product.category_id:
            category = await self.category_repository.get_by_id(data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found"
                )
            product.category_id = data.category_id

        update_data = data.model_dump(exclude_unset=True, exclude={"category_id"})
        for field, value in update_data.items():
            setattr(product, field, value)

        try:
            await self.repository.update(product)
            await self.session.commit()
            return product
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists"
            )

    async def delete_product(self, product_id: int) -> None:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        product.is_deleted = True
        product.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await self.repository.update(product)
        await self.session.commit()
