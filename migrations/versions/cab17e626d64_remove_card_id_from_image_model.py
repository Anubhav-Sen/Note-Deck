"""remove card_id from image model

Revision ID: cab17e626d64
Revises: c23bfeb6ea55
Create Date: 2022-04-29 20:04:56.352125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cab17e626d64'
down_revision = 'c23bfeb6ea55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'image', type_='foreignkey')
    op.drop_column('image', 'card_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('card_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key(None, 'image', 'card', ['card_id'], ['id'])
    # ### end Alembic commands ###
