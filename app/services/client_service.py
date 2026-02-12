"""Client business logic: CRUD and soft delete."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    """Client CRUD; enforces unique email and soft delete."""

    def __init__(self, session: AsyncSession):
        self.repository = ClientRepository(session)
        self.session = session

    async def create_client(self, data: ClientCreate) -> Client:
        existing = await self.repository.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client with this email already exists"
            )

        new_client = Client(**data.model_dump())
        try:
            await self.repository.create(new_client)
            await self.session.commit()
            return new_client
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client with this email already exists"
            )

    async def get_client(self, client_id: int) -> Client:
        client = await self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        return client

    async def get_clients(self, offset: int = 0, limit: int = 100) -> list[Client]:
        return await self.repository.get_all(offset, limit)

    async def update_client(self, client_id: int, data: ClientUpdate) -> Client:
        client = await self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        if data.email and data.email != client.email:
            existing = await self.repository.get_by_email(data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Client with this email already exists"
                )

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)

        try:
            await self.repository.update(client)
            await self.session.commit()
            return client
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client with this email already exists"
            )

    async def delete_client(self, client_id: int) -> None:
        client = await self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        client.is_deleted = True
        client.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await self.repository.update(client)
        await self.session.commit()
