"""Create Entities

Revision ID: afedd2251b75
Revises: 
Create Date: 2022-03-25 17:13:31.901294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afedd2251b75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('album',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('artist', sa.String(length=120), nullable=True),
    sa.Column('launch_year', sa.Integer(), nullable=True),
    sa.Column('style', sa.String(length=120), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_album_artist'), 'album', ['artist'], unique=False)
    op.create_index(op.f('ix_album_launch_year'), 'album', ['launch_year'], unique=False)
    op.create_index(op.f('ix_album_name'), 'album', ['name'], unique=False)
    op.create_index(op.f('ix_album_style'), 'album', ['style'], unique=False)
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document', sa.String(length=120), nullable=True),
    sa.Column('full_name', sa.String(length=120), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('album_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_table('client')
    op.drop_index(op.f('ix_album_style'), table_name='album')
    op.drop_index(op.f('ix_album_name'), table_name='album')
    op.drop_index(op.f('ix_album_launch_year'), table_name='album')
    op.drop_index(op.f('ix_album_artist'), table_name='album')
    op.drop_table('album')
    # ### end Alembic commands ###
