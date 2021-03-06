"""empty message

Revision ID: 948d9ce99479
Revises: bdee130788ce
Create Date: 2018-11-25 20:18:25.107028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '948d9ce99479'
down_revision = 'bdee130788ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_tags',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_tags')
    # ### end Alembic commands ###
