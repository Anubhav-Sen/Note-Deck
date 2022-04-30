"""add image_id to card model

Revision ID: 16ae06231d64
Revises: 1aabb4f7c0dd
Create Date: 2022-04-29 20:23:47.956191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16ae06231d64'
down_revision = '1aabb4f7c0dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('image_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'card', 'image', ['image_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'card', type_='foreignkey')
    op.drop_column('card', 'image_id')
    # ### end Alembic commands ###