"""create Order table

Revision ID: 2275d54f5ea4
Revises: 
Create Date: 2024-02-26 00:47:57.306634

"""
from typing import Sequence, Union
from datetime import datetime
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2275d54f5ea4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'order',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('dish', sa.String(50), nullable=False),
        sa.Column('cost', sa.Float),
        sa.Column('data', sa.DateTime, default=datetime.now),
        sa.Column('comment', sa.String(500)),
        sa.Column('client_id', sa.ForeignKey("client.id"))
    )
    op.create_table(
        'dishe',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('cost', sa.Float),
        sa.Column('type', sa.String(20)),
        sa.Column('description', sa.String(500)),
        sa.Column('restaurant_id', sa.ForeignKey("restaurant.id"))
    )
    op.create_table(
        'dishe_order',
        sa.Column('dishe_id', sa.ForeignKey("dishe.id")),
        sa.Column('order_id', sa.ForeignKey("order_id")),
    )


def downgrade() -> None:
    pass
