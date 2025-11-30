"""Create Search Vector

Revision ID: ebaa7e8fbf05
Revises: e80355e217cd
Create Date: 2025-11-30 17:28:34.386864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ebaa7e8fbf05'
down_revision: Union[str, Sequence[str], None] = 'e80355e217cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('tsv', postgresql.TSVECTOR(), sa.Computed("\n            setweight(to_tsvector('english', coalesce(name, '')), 'A')\n            || \n            setweight(to_tsvector('english', coalesce(description, '')), 'B')\n            ", persisted=True), nullable=False))
    op.create_index('ix_products_tsv_gin', 'products', ['tsv'], unique=False, postgresql_using='gin')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_products_tsv_gin', table_name='products', postgresql_using='gin')
    op.drop_column('products', 'tsv')
