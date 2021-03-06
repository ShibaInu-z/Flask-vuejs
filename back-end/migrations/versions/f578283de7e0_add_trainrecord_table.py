"""add TrainRecord table

Revision ID: f578283de7e0
Revises: 807a5f3cfd23
Create Date: 2021-04-29 10:50:16.025915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f578283de7e0'
down_revision = '807a5f3cfd23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trainRecords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('app_name', sa.String(length=128), nullable=False),
    sa.Column('utc_str', sa.String(length=128), nullable=False),
    sa.Column('VGG_paras', sa.JSON(), nullable=True),
    sa.Column('logs', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trainRecords')
    # ### end Alembic commands ###
