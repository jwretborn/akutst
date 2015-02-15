"""empty message

Revision ID: 7e7882a4d5e
Revises: None
Create Date: 2015-02-15 17:14:55.526466

"""

# revision identifiers, used by Alembic.
revision = '7e7882a4d5e'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('procedures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=10), nullable=True),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('created', sa.Date(), nullable=True),
    sa.Column('successful', sa.Boolean(), nullable=True),
    sa.Column('attempts', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('procedures')
    ### end Alembic commands ###
