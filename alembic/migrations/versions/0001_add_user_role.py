"""Add role to users.

Revision ID: 0001_add_user_role
Revises:
Create Date: 2026-01-28 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_add_user_role"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    role_enum = sa.Enum("admin", "member", name="userrole")
    role_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "users",
        sa.Column(
            "role",
            role_enum,
            nullable=False,
            server_default=sa.text("'member'"),
        ),
    )
    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "role")
    role_enum = sa.Enum("admin", "member", name="userrole")
    role_enum.drop(op.get_bind(), checkfirst=True)
