"""Create organization-scoped products.

Revision ID: 0002_products
Revises: 0001_registration
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_products"
down_revision: Union[str, None] = "0001_registration"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "quantity_on_hand",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("cost_price", sa.Numeric(12, 2), nullable=True),
        sa.Column("selling_price", sa.Numeric(12, 2), nullable=True),
        sa.Column("low_stock_threshold", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "sku",
            name="uq_products_organization_sku",
        ),
        sa.CheckConstraint(
            "quantity_on_hand >= 0",
            name="ck_products_quantity_nonnegative",
        ),
        sa.CheckConstraint(
            "cost_price IS NULL OR cost_price >= 0",
            name="ck_products_cost_price_nonnegative",
        ),
        sa.CheckConstraint(
            "selling_price IS NULL OR selling_price >= 0",
            name="ck_products_selling_price_nonnegative",
        ),
        sa.CheckConstraint(
            "low_stock_threshold IS NULL OR low_stock_threshold >= 0",
            name="ck_products_threshold_nonnegative",
        ),
    )
    op.create_index(
        "ix_products_organization_id",
        "products",
        ["organization_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_products_organization_id", table_name="products")
    op.drop_table("products")
