"""Pending fiction images

Revision ID: 36ec2e4c6e83
Revises: 0334f408ae0a
Create Date: 2020-09-08 07:23:30.192011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36ec2e4c6e83'
down_revision = '0334f408ae0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fiction', sa.Column('pending_banner_img', sa.String(length=500), nullable=True))
    op.add_column('fiction', sa.Column('pending_cover_img', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fiction', 'pending_cover_img')
    op.drop_column('fiction', 'pending_banner_img')
    # ### end Alembic commands ###
