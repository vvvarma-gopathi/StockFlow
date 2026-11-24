"""Add persistent stock adjustment history.

Revision ID: 0003_stock_adjustments
Revises: 0002_products
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_stock_adjustments"
down_revision: Union[str, None] = "0002_products"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stock_adjustments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("adjusted_by_user_id", sa.Integer(), nullable=True),
        sa.Column("quantity_delta", sa.Integer(), nullable=False),
        sa.Column("previous_quantity", sa.Integer(), nullable=False),
        sa.Column("quantity_after", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["adjusted_by_user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.CheckConstraint(
            "quantity_delta != 0",
            name="ck_stock_adjustments_delta_nonzero",
        ),
        sa.CheckConstraint(
            "previous_quantity >= 0 AND quantity_after >= 0",
            name="ck_stock_adjustments_quantities_nonnegative",
        ),
        sa.CheckConstraint(
            "quantity_after = previous_quantity + quantity_delta",
            name="ck_stock_adjustments_quantity_delta_consistent",
        ),
    )
    op.create_index(
        "ix_stock_adjustments_product_created_at",
        "stock_adjustments",
        ["product_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_stock_adjustments_product_created_at",
        table_name="stock_adjustments",
    )
    op.drop_table("stock_adjustments")
