"""Add organization low-stock fallback settings.

Revision ID: 0004_low_stock_settings
Revises: 0003_stock_adjustments
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_low_stock_settings"
down_revision: Union[str, None] = "0003_stock_adjustments"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "organizations",
        sa.Column(
            "default_low_stock_threshold_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "organizations",
        "default_low_stock_threshold_enabled",
    )
