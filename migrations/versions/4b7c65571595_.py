"""empty message

Revision ID: 4b7c65571595
Revises: 5657d9f6d96d
Create Date: 2016-04-01 08:33:53.774237

"""

# revision identifiers, used by Alembic.
revision = '4b7c65571595'
down_revision = '5657d9f6d96d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('ALTER TABLE users ALTER COLUMN login_count TYPE integer USING (login_count::integer)')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'login_count',
                existing_type=sa.INTEGER(), type_=sa.String(50))
    ### end Alembic commands ###
