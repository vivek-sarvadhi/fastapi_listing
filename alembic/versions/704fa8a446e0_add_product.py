"""add product

Revision ID: 704fa8a446e0
Revises: 974ed4fe98b8
Create Date: 2023-04-20 12:56:44.487879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '704fa8a446e0'
down_revision = '974ed4fe98b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('category_id', sa.Integer(), nullable=False))
    op.add_column('product', sa.Column('brand_id', sa.Integer(), nullable=False))
    op.add_column('product', sa.Column('hsn_code', sa.Integer(), nullable=False))
    op.add_column('product', sa.Column('dimensions', sa.String(), nullable=False))
    op.add_column('product', sa.Column('price', sa.Float(), nullable=False))
    op.add_column('product', sa.Column('image', sa.String(), nullable=False))
    op.drop_constraint('product_data_key', 'product', type_='unique')
    op.drop_constraint('product_name_key', 'product', type_='unique')
    op.create_foreign_key(None, 'product', 'category', ['category_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'product', 'brand', ['brand_id'], ['id'], ondelete='CASCADE')
    op.drop_column('product', 'data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('data', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.create_unique_constraint('product_name_key', 'product', ['name'])
    op.create_unique_constraint('product_data_key', 'product', ['data'])
    op.drop_column('product', 'image')
    op.drop_column('product', 'price')
    op.drop_column('product', 'dimensions')
    op.drop_column('product', 'hsn_code')
    op.drop_column('product', 'brand_id')
    op.drop_column('product', 'category_id')
    # ### end Alembic commands ###