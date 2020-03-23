"""New submissions

Revision ID: bc66135d3775
Revises: 4292e74da773
Create Date: 2020-03-22 12:59:28.151034

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bc66135d3775'
down_revision = '4292e74da773'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fiction_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('fiction_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fiction_id'], ['fiction.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'fiction_id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('submission_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=5000), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('hidden', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proposal_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'submission_id')
    )
    op.add_column('fiction', sa.Column('rating', sa.String(length=20), nullable=False))
    op.add_column('link', sa.Column('submission_id', sa.Integer(), nullable=True))
    op.alter_column('link', 'fiction_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.create_foreign_key(None, 'link', 'submission', ['submission_id'], ['id'])
    op.add_column('submission', sa.Column('approval', sa.Boolean(), nullable=True))
    op.add_column('submission', sa.Column('approval_date', sa.DateTime(), nullable=True))
    op.add_column('submission', sa.Column('approver_id', sa.Integer(), nullable=True))
    op.add_column('submission', sa.Column('author_id', sa.Integer(), nullable=True))
    op.add_column('submission', sa.Column('author_placeholder', sa.String(length=100), nullable=True))
    op.add_column('submission', sa.Column('banner_img', sa.String(length=500), nullable=True))
    op.add_column('submission', sa.Column('cover_img', sa.String(length=500), nullable=True))
    op.add_column('submission', sa.Column('frequency', sa.Float(), nullable=True))
    op.add_column('submission', sa.Column('rating', sa.String(length=20), nullable=False))
    op.add_column('submission', sa.Column('status', sa.String(length=75), nullable=False))
    op.add_column('submission', sa.Column('subtitle', sa.String(length=150), nullable=True))
    op.add_column('submission', sa.Column('synopsis', sa.String(length=1000), nullable=False))
    op.add_column('submission', sa.Column('title', sa.String(length=150), nullable=False))
    op.add_column('submission', sa.Column('website', sa.String(length=300), nullable=False))
    op.add_column('submission', sa.Column('words', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'submission', 'user', ['approver_id'], ['id'])
    op.create_foreign_key(None, 'submission', 'user', ['author_id'], ['id'])
    op.drop_column('submission', 'response')
    op.drop_column('submission', 'type')
    op.drop_column('submission', 'path')
    op.drop_column('submission', 'comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submission', sa.Column('comment', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=1000), nullable=True))
    op.add_column('submission', sa.Column('path', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=500), nullable=False))
    op.add_column('submission', sa.Column('type', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=50), nullable=False))
    op.add_column('submission', sa.Column('response', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'submission', type_='foreignkey')
    op.drop_constraint(None, 'submission', type_='foreignkey')
    op.drop_column('submission', 'words')
    op.drop_column('submission', 'website')
    op.drop_column('submission', 'title')
    op.drop_column('submission', 'synopsis')
    op.drop_column('submission', 'subtitle')
    op.drop_column('submission', 'status')
    op.drop_column('submission', 'rating')
    op.drop_column('submission', 'frequency')
    op.drop_column('submission', 'cover_img')
    op.drop_column('submission', 'banner_img')
    op.drop_column('submission', 'author_placeholder')
    op.drop_column('submission', 'author_id')
    op.drop_column('submission', 'approver_id')
    op.drop_column('submission', 'approval_date')
    op.drop_column('submission', 'approval')
    op.drop_constraint(None, 'link', type_='foreignkey')
    op.alter_column('link', 'fiction_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column('link', 'submission_id')
    op.drop_column('fiction', 'rating')
    op.drop_table('proposal_tags')
    op.drop_table('comment')
    op.drop_table('fiction_tags')
    # ### end Alembic commands ###