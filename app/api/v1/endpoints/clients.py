from fastapi import APIRouter, Depends, Query

from app.api.deps import get_client_service
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.services.client_service import ClientService


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=ClientResponse, status_code=201)
async def create_client(
    data: ClientCreate,
    service: ClientService = Depends(get_client_service)
):
    return await service.create_client(data)


@router.get("/", response_model=list[ClientResponse])
async def get_clients(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: ClientService = Depends(get_client_service)
):
    return await service.get_clients(offset, limit)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    service: ClientService = Depends(get_client_service)
):
    return await service.get_client(client_id)


@router.patch("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    data: ClientUpdate,
    service: ClientService = Depends(get_client_service)
):
    return await service.update_client(client_id, data)


@router.delete("/{client_id}", status_code=204)
async def delete_client(
    client_id: int,
    service: ClientService = Depends(get_client_service)
):
    await service.delete_client(client_id)
