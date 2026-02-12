from fastapi import APIRouter, Depends, Query

from app.api.deps import get_order_service
from app.core.enums import OrderStatus
from app.schemas.order import OrderProductAdd, OrderProductAddBatch, OrderResponse
from app.services.order_service import OrderService


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    client_id: int,
    service: OrderService = Depends(get_order_service)
):
    order = await service.create_order(client_id)
    return OrderResponse.from_order(order)


@router.get("/", response_model=list[OrderResponse])
async def get_orders(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: OrderService = Depends(get_order_service)
):
    orders = await service.get_orders(offset, limit)
    return [OrderResponse.from_order(order) for order in orders]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
):
    order = await service.get_order(order_id)
    return OrderResponse.from_order(order)


@router.post("/{order_id}/items", response_model=OrderResponse)
async def add_item_to_order(
    order_id: int,
    item_data: OrderProductAdd,
    service: OrderService = Depends(get_order_service)
):
    order = await service.add_item_to_order(order_id, item_data)
    return OrderResponse.from_order(order)


@router.post("/{order_id}/items/batch", response_model=OrderResponse)
async def add_items_to_order(
    order_id: int,
    batch: OrderProductAddBatch,
    service: OrderService = Depends(get_order_service)
):
    """Add multiple products to an order in one request."""
    order = await service.add_items_to_order(order_id, batch.items)
    return OrderResponse.from_order(order)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    service: OrderService = Depends(get_order_service)
):
    order = await service.update_order_status(order_id, status)
    return OrderResponse.from_order(order)


@router.delete("/{order_id}", status_code=204)
async def delete_order(
    order_id: int,
    service: OrderService = Depends(get_order_service)
):
    await service.delete_order(order_id)
