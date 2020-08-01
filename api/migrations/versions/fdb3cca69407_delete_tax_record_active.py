"""delete tax_record -> active

Revision ID: fdb3cca69407
Revises: 241cdedc0a02
Create Date: 2020-08-01 09:05:41.329704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdb3cca69407'
down_revision = '241cdedc0a02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tax_record', 'active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tax_record', sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
