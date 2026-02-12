from fastapi import APIRouter, Depends, Query

from app.api.deps import get_category_service
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryTreeResponse
from app.services.category_service import CategoryService


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    return await service.create_category(data)


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_categories(offset, limit)


@router.get("/roots", response_model=list[CategoryTreeResponse])
async def get_root_categories(
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_root_categories()


@router.get("/{category_id}", response_model=CategoryTreeResponse)
async def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_category(category_id)


@router.get("/{category_id}/children", response_model=list[CategoryTreeResponse])
async def get_category_children(
    category_id: int,
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_category_children(category_id)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    return await service.update_category(category_id, data)


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service)
):
    await service.delete_category(category_id)
