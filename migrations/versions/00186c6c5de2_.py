"""empty message

Revision ID: 00186c6c5de2
Revises: 41ade387a278
Create Date: 2020-02-09 14:42:50.522376

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '00186c6c5de2'
down_revision = '41ade387a278'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_chat_log', sa.Column('isread', sa.Boolean(), nullable=True))
    op.drop_column('user_chat_log', 'has_read')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_chat_log', sa.Column('has_read', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('user_chat_log', 'isread')
    # ### end Alembic commands ###
