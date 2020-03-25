"""Rating can be null

Revision ID: ba9006ee6ac1
Revises: e4a77e69e09e
Create Date: 2020-03-23 18:32:18.573381

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ba9006ee6ac1'
down_revision = 'e4a77e69e09e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('fiction', 'rating',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
               nullable=True)
    op.alter_column('submission', 'rating',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submission', 'rating',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
               nullable=False)
    op.alter_column('fiction', 'rating',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20),
               nullable=False)
    # ### end Alembic commands ###