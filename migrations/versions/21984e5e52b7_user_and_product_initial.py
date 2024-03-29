"""Initial migration, user and product tables

Revision ID: 21984e5e52b7
Revises: 
Create Date: 2022-09-05 00:31:22.054983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21984e5e52b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('product',
        sa.Column('p_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=True),
        sa.Column('price', sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint('p_id')
    )
    op.create_index(op.f('ix_product_name'), 'product', ['name'], unique=False)
    op.create_table('user',
        sa.Column('s_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=32), nullable=True),
        sa.Column('last_name', sa.String(length=32), nullable=True),
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('password', sa.String(length=32), nullable=True),
        sa.Column('permissions', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('s_id'),
        sa.UniqueConstraint('student_id')
    )
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_student_id'), 'user', ['student_id'], unique=True)


def downgrade():
    op.drop_table('user')
    op.drop_table('product')
