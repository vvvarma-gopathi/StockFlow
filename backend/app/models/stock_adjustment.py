from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base


class StockAdjustment(Base):
    __tablename__ = "stock_adjustments"
    __table_args__ = (
        CheckConstraint(
            "quantity_delta != 0",
            name="ck_stock_adjustments_delta_nonzero",
        ),
        CheckConstraint(
            "previous_quantity >= 0 AND quantity_after >= 0",
            name="ck_stock_adjustments_quantities_nonnegative",
        ),
        CheckConstraint(
            "quantity_after = previous_quantity + quantity_delta",
            name="ck_stock_adjustments_quantity_delta_consistent",
        ),
        Index(
            "ix_stock_adjustments_product_created_at",
            "product_id",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    adjusted_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    quantity_delta: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity_after: Mapped[int] = mapped_column(Integer, nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        back_populates="stock_adjustments"
    )
