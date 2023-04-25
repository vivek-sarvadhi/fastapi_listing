"""Initial migration

Revision ID: 137e2b1038f8
Revises: f898f1df41ae
Create Date: 2023-04-21 14:12:05.906452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '137e2b1038f8'
down_revision = 'f898f1df41ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('data', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'data')
    # ### end Alembic commands ###
