from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from app.core.enums import OrderStatus
from app.db.models.order import Order


class OrderProductAdd(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity to add to the order")


class OrderProductAddBatch(BaseModel):
    """Add multiple items to an order in one request."""
    items: list[OrderProductAdd] = Field(..., min_length=1, max_length=100)


class OrderProductResponse(BaseModel):
    product_id: int
    name: str | None = None
    quantity: int
    price_at_order: Decimal
    
    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    client_id: int
    status: OrderStatus
    items: list[OrderProductResponse] = Field(alias="order_products")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @classmethod
    def from_order(cls, order: "Order") -> "OrderResponse":
        """Build OrderResponse from an Order model (with order_products loaded)."""
        return cls(
            id=order.id,
            client_id=order.client_id,
            status=order.status,
            order_products=[
                OrderProductResponse(
                    product_id=op.product_id,
                    name=op.product.name if op.product else None,
                    quantity=op.quantity,
                    price_at_order=op.price_at_order,
                )
                for op in order.order_products
            ],
        )
