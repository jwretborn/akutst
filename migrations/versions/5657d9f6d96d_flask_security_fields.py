"""Flask-security fields

Revision ID: 5657d9f6d96d
Revises: 1d77ec8f3267
Create Date: 2016-02-13 18:45:22.700014

"""

# revision identifiers, used by Alembic.
revision = '5657d9f6d96d'
down_revision = '1d77ec8f3267'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # User table stuff #
    op.add_column('users', sa.Column('first_name', sa.String(length=255)))
    op.add_column('users', sa.Column('last_name', sa.String(length=255)))
    op.add_column('users', sa.Column('email', sa.String(length=255), unique=True))
    op.add_column('users', sa.Column('password', sa.String(length=255)))
    op.add_column('users', sa.Column('active', sa.Boolean()))
    op.add_column('users', sa.Column('confirmed_at', sa.DateTime()))
    op.add_column('users', sa.Column('last_login_at', sa.DateTime()))
    op.add_column('users', sa.Column('current_login_at', sa.String(50)))
    op.add_column('users', sa.Column('login_count', sa.String(50)))

    # Add Role table #
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), unique=False),
    sa.Column('description', sa.String(length=255)),
    sa.PrimaryKeyConstraint('id')
    )
    pass


def downgrade():
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'email')
    op.drop_column('users', 'password')
    op.drop_column('users', 'active')
    op.drop_column('users', 'confirmed_at')
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'current_login_at')
    op.drop_column('users', 'login_count')

    op.drop_table('roles')
    pass
