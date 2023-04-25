"""add data2 in product

Revision ID: 15cd5b2684c5
Revises: 62a6f3800085
Create Date: 2023-04-21 14:57:25.910590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15cd5b2684c5'
down_revision = '62a6f3800085'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('data2', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'data2')
    # ### end Alembic commands ###