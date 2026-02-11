from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, SoftDeleteMixin


class Product(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        index=True
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    order_products: Mapped[list["OrderProduct"]] = relationship("OrderProduct", back_populates="product")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_product_quantity_positive"),
    )
