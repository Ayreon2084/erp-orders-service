from fastapi import APIRouter, Depends, Query

from app.api.deps import get_product_service
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    return await service.create_product(data)


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: ProductService = Depends(get_product_service)
):
    return await service.get_products(offset, limit)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    return await service.get_product(product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    return await service.update_product(product_id, data)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    await service.delete_product(product_id)
