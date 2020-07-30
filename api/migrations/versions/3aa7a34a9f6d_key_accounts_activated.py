"""key_accounts activated

Revision ID: 3aa7a34a9f6d
Revises: 
Create Date: 2020-07-30 06:33:44.971007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa7a34a9f6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tax_auditor_seller_firm_AT',
    sa.Column('tax_auditor_id', sa.Integer(), nullable=False),
    sa.Column('seller_firm_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['seller_firm_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['tax_auditor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('tax_auditor_id', 'seller_firm_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tax_auditor_seller_firm_AT')
    # ### end Alembic commands ###
