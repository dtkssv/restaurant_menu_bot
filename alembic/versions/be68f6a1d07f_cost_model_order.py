"""cost -> model order

Revision ID: be68f6a1d07f
Revises: e69987ad09ce
Create Date: 2024-04-04 07:10:31.243869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be68f6a1d07f'
down_revision: Union[str, None] = 'e69987ad09ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('cost', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'cost')
    # ### end Alembic commands ###
