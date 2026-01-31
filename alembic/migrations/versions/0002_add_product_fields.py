"""Add product category and status.

Revision ID: 0002_add_product_fields
Revises: 0001_add_user_role
Create Date: 2026-01-29 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_add_product_fields"
down_revision = "0001_add_user_role"
branch_labels = None
depends_on = None


def upgrade() -> None:
    category_enum = sa.Enum("food", "drink", "other", name="productcategory")
    status_enum = sa.Enum("available", "unavailable", name="productstatus")
    category_enum.create(op.get_bind(), checkfirst=True)
    status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "products",
        sa.Column(
            "product_category",
            category_enum,
            nullable=False,
            server_default=sa.text("'other'"),
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "status",
            status_enum,
            nullable=False,
            server_default=sa.text("'available'"),
        ),
    )
    op.alter_column("products", "product_category", server_default=None)
    op.alter_column("products", "status", server_default=None)


def downgrade() -> None:
    op.drop_column("products", "status")
    op.drop_column("products", "product_category")

    status_enum = sa.Enum("available", "unavailable", name="productstatus")
    category_enum = sa.Enum("food", "drink", "other", name="productcategory")
    status_enum.drop(op.get_bind(), checkfirst=True)
    category_enum.drop(op.get_bind(), checkfirst=True)
