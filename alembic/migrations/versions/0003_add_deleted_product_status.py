"""Add deleted product status.

Revision ID: 0003_add_deleted_product_status
Revises: 0002_add_product_fields
Create Date: 2026-01-29 00:00:00.000000
"""

from alembic import op


revision = "0003_add_deleted_product_status"
down_revision = "0002_add_product_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE productstatus ADD VALUE IF NOT EXISTS 'deleted'")


def downgrade() -> None:
    # PostgreSQL cannot remove enum values easily; leave as-is.
    pass
