"""empty message

Revision ID: 510d7137376f
Revises: 17fa3622a0ad
Create Date: 2015-03-15 21:14:55.106304

"""

# revision identifiers, used by Alembic.
revision = '510d7137376f'
down_revision = '17fa3622a0ad'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'procedures_method_id_fkey', 'procedures', type_='foreignkey')
    op.drop_constraint(u'procedures_anatomy_id_fkey', 'procedures', type_='foreignkey')
    op.create_foreign_key(None, 'procedures', 'group_items', ['anatomy_id'], ['id'])
    op.create_foreign_key(None, 'procedures', 'group_items', ['method_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'procedures', type_='foreignkey')
    op.drop_constraint(None, 'procedures', type_='foreignkey')
    op.create_foreign_key(u'procedures_anatomy_id_fkey', 'procedures', 'groups', ['anatomy_id'], ['id'])
    op.create_foreign_key(u'procedures_method_id_fkey', 'procedures', 'groups', ['method_id'], ['id'])
    ### end Alembic commands ###
