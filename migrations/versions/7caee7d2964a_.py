"""empty message

Revision ID: 7caee7d2964a
Revises: f511298d7f30
Create Date: 2018-12-12 20:31:32.099569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7caee7d2964a'
down_revision = 'f511298d7f30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=64), nullable=True),
    sa.Column('company', sa.String(length=256), nullable=True),
    sa.Column('exchange', sa.String(length=128), nullable=True),
    sa.Column('industry', sa.String(length=128), nullable=True),
    sa.Column('website', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('CEO', sa.String(length=128), nullable=True),
    sa.Column('issueType', sa.String(length=128), nullable=True),
    sa.Column('sector', sa.String(length=128), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_company'), 'companies', ['company'], unique=True)
    op.create_index(op.f('ix_companies_symbol'), 'companies', ['symbol'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_companies_symbol'), table_name='companies')
    op.drop_index(op.f('ix_companies_company'), table_name='companies')
    op.drop_table('companies')
    # ### end Alembic commands ###
