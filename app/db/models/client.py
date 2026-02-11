from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, SoftDeleteMixin


class Client(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "clients"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="client")
