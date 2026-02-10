"""Async database session configuration."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings



engine = create_async_engine(settings.database_url, echo=settings.debug)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session.

    Yields:
        Async database session instance.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
