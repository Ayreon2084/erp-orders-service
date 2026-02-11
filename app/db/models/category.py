from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, SoftDeleteMixin


class Category(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), 
        nullable=True,
        index=True
    )

    # Each category can have one parent and many children (self-referential relationship)
    parent: Mapped["Category | None"] = relationship(
        "Category", 
        back_populates="children", 
        remote_side="Category.id"
    )
    children: Mapped[list["Category"]] = relationship(
        "Category", 
        back_populates="parent"
    )

    products: Mapped[list["Product"]] = relationship(
        "Product", 
        back_populates="category"
    )
