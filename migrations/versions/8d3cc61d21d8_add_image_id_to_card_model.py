"""add image_id to card model

Revision ID: 8d3cc61d21d8
Revises: 16ae06231d64
Create Date: 2022-04-29 20:27:27.402797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d3cc61d21d8'
down_revision = '16ae06231d64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'card', 'image', ['image_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'card', type_='foreignkey')
    # ### end Alembic commands ###
