"""попытка 5

Revision ID: b24f6bcd06d8
Revises: ee4ec1d0d602
Create Date: 2024-04-01 18:29:27.217501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b24f6bcd06d8'
down_revision: Union[str, None] = 'ee4ec1d0d602'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Dish_Order', 'dish_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Dish_Order', 'order_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Dish_Order', 'order_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Dish_Order', 'dish_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
