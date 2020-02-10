"""empty message

Revision ID: 41ade387a278
Revises: 0e10d8a3a510
Create Date: 2020-02-08 17:03:39.092954

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '41ade387a278'
down_revision = '0e10d8a3a510'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('contact_id', sa.Integer(), nullable=True))
    op.drop_constraint('user_ibfk_1', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'user', ['contact_id'], ['id'])
    op.drop_column('user', 'friend_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('friend_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_ibfk_1', 'user', 'user', ['friend_id'], ['id'])
    op.drop_column('user', 'contact_id')
    # ### end Alembic commands ###
