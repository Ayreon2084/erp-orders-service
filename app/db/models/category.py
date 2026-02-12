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
    # Denormalization: root_category_id for reports without recursive CTEs
    root_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )

    # Parent/children: use parent_id only (self-referential).
    parent: Mapped["Category | None"] = relationship(
        "Category",
        back_populates="children",
        foreign_keys=[parent_id],
        remote_side="Category.id",
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
        foreign_keys=[parent_id],
    )
    root_category: Mapped["Category | None"] = relationship(
        "Category",
        foreign_keys=[root_category_id],
        remote_side="Category.id",
    )

    products: Mapped[list["Product"]] = relationship(
        "Product", 
        back_populates="category"
    )
