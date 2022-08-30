"""add order and orderproduct tables

Revision ID: 3149c26fcfee
Revises: 21984e5e52b7
Create Date: 2022-09-25 20:35:32.710135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3149c26fcfee'
down_revision = '21984e5e52b7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('order',
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('date_of_creation', sa.DateTime(), nullable=True),
        sa.Column('target_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.s_id'], ),
        sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('order_product',
        sa.Column('order_id', sa.Integer(), nullable=True),
        sa.Column('p_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
        sa.ForeignKeyConstraint(['p_id'], ['product.p_id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('order')
    op.drop_table('order_product')