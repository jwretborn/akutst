"""empty message

Revision ID: 7ca6d1f7b1f5
Revises: 9ba3a5b62007
Create Date: 2017-02-26 16:49:06.032210

"""

# revision identifiers, used by Alembic.
revision = '7ca6d1f7b1f5'
down_revision = '9ba3a5b62007'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], name='patient_tags_patient_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='patient_tags_tag_id_fkey')
    )
    op.create_table('procedure_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('procedure_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['procedure_id'], ['procedures.id'], name='procedure_tags_procedure_id_fkey'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='procedure_tags_tag_id_fkey')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('procedure_tags')
    op.drop_table('patient_tags')
    op.drop_table('tags')
    ### end Alembic commands ###
