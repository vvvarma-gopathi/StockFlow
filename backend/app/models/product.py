from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.stock_adjustment import StockAdjustment


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "sku",
            name="uq_products_organization_sku",
        ),
        CheckConstraint(
            "quantity_on_hand >= 0",
            name="ck_products_quantity_nonnegative",
        ),
        CheckConstraint(
            "cost_price IS NULL OR cost_price >= 0",
            name="ck_products_cost_price_nonnegative",
        ),
        CheckConstraint(
            "selling_price IS NULL OR selling_price >= 0",
            name="ck_products_selling_price_nonnegative",
        ),
        CheckConstraint(
            "low_stock_threshold IS NULL OR low_stock_threshold >= 0",
            name="ck_products_threshold_nonnegative",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity_on_hand: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    cost_price: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2), nullable=True
    )
    selling_price: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2), nullable=True
    )
    low_stock_threshold: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="products"
    )
    stock_adjustments: Mapped[list["StockAdjustment"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )

    @property
    def effective_low_stock_threshold(self) -> int | None:
        if self.low_stock_threshold is not None:
            return self.low_stock_threshold
        if self.organization.default_low_stock_threshold_enabled:
            return self.organization.default_low_stock_threshold
        return None

    @property
    def is_low_stock(self) -> bool:
        threshold = self.effective_low_stock_threshold
        return threshold is not None and self.quantity_on_hand <= threshold