from enum import StrEnum


class OrderStatus(StrEnum):
    """Order lifecycle status."""

    NEW = "new"
    PROCESSING = "processing"
    PAID = "paid"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
