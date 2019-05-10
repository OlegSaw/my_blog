"""empty message

Revision ID: 87dc92a45bb7
Revises: 7f3c0a576da3
Create Date: 2018-12-23 01:26:49.819986

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '87dc92a45bb7'
down_revision = '7f3c0a576da3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_ibfk_2', 'users', type_='foreignkey')
    op.drop_constraint('users_ibfk_1', 'users', type_='foreignkey')
    op.drop_column('users', 'user_id')
    op.drop_column('users', 'role_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('users_ibfk_1', 'users', 'users', ['role_id'], ['id'])
    op.create_foreign_key('users_ibfk_2', 'users', 'roles', ['user_id'], ['id'])
    # ### end Alembic commands ###