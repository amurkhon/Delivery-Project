"""change quantity to volume enum

Revision ID: 0004_qty_to_volume
Revises: 0003_add_deleted_product_status
Create Date: 2026-01-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0004_qty_to_volume'
down_revision: Union[str, None] = '0003_add_deleted_product_status'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the volume enum type
    volume_enum = sa.Enum('small', 'medium', 'large', name='volume')
    volume_enum.create(op.get_bind(), checkfirst=True)
    
    # Drop the old quantity column
    op.drop_column('products', 'quantity')
    
    # Add the new volume column with enum type
    op.add_column('products', 
        sa.Column('volume', sa.Enum('small', 'medium', 'large', name='volume'), 
                  nullable=False, server_default='small')
    )


def downgrade() -> None:
    # Drop the volume column
    op.drop_column('products', 'volume')
    
    # Add back the quantity column
    op.add_column('products',
        sa.Column('quantity', sa.Integer(), nullable=True, server_default='0')
    )
    
    # Drop the volume enum type
    op.execute('DROP TYPE IF EXISTS volume')
