"""FastAPI dependencies: session and service factories."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.services.category_service import CategoryService
from app.services.client_service import ClientService
from app.services.order_service import OrderService
from app.services.product_service import ProductService


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_category_service(db: SessionDep) -> CategoryService:
    return CategoryService(db)


def get_product_service(db: SessionDep) -> ProductService:
    return ProductService(db)


def get_client_service(db: SessionDep) -> ClientService:
    return ClientService(db)


def get_order_service(db: SessionDep) -> OrderService:
    return OrderService(db)
