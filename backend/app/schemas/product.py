from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    sku: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    quantity_on_hand: int = Field(default=0, ge=0)
    cost_price: Decimal | None = Field(
        default=None, ge=0, max_digits=12, decimal_places=2
    )
    selling_price: Decimal | None = Field(
        default=None, ge=0, max_digits=12, decimal_places=2
    )
    low_stock_threshold: int | None = Field(default=None, ge=0)

    @field_validator("name", "sku")
    @classmethod
    def normalize_required_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class ProductUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    sku: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    quantity_on_hand: int = Field(ge=0)
    cost_price: Decimal | None = Field(
        default=None, ge=0, max_digits=12, decimal_places=2
    )
    selling_price: Decimal | None = Field(
        default=None, ge=0, max_digits=12, decimal_places=2
    )
    low_stock_threshold: int | None = Field(default=None, ge=0)

    @field_validator("name", "sku")
    @classmethod
    def normalize_required_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    name: str
    sku: str
    description: str | None
    quantity_on_hand: int
    cost_price: Decimal | None
    selling_price: Decimal | None
    low_stock_threshold: int | None
    effective_low_stock_threshold: int | None
    is_low_stock: bool
    created_at: datetime
    updated_at: datetime


class StockAdjustmentCreate(BaseModel):
    quantity_delta: int
    note: str = Field(min_length=1, max_length=500)

    @field_validator("quantity_delta")
    @classmethod
    def reject_zero_delta(cls, value: int) -> int:
        if value == 0:
            raise ValueError("Quantity change must not be zero.")
        return value

    @field_validator("note")
    @classmethod
    def normalize_note(cls, value: str) -> str:
        note = value.strip()
        if not note:
            raise ValueError("A note is required.")
        return note


class StockAdjustmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    adjusted_by_user_id: int | None
    quantity_delta: int
    previous_quantity: int
    quantity_after: int
    note: str
    created_at: datetime