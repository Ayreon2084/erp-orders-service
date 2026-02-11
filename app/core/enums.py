from enum import StrEnum


class OrderStatus(StrEnum):
    NEW = "new"
    PROCESSING = "processing"
    PAID = "paid"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
