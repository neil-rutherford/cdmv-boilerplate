"""First commit

Revision ID: 2a86a4bf289d
Revises: 
Create Date: 2021-10-20 11:28:11.805024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a86a4bf289d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=300), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('author_name', sa.String(length=70), nullable=True),
    sa.Column('author_handle', sa.String(length=70), nullable=True),
    sa.Column('title', sa.String(length=70), nullable=True),
    sa.Column('description', sa.String(length=155), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('section', sa.String(length=50), nullable=True),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.Column('image_url', sa.String(length=300), nullable=True),
    sa.Column('published_time', sa.DateTime(), nullable=True),
    sa.Column('modified_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_slug'), 'content', ['slug'], unique=True)
    op.create_table('lead',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=35), nullable=True),
    sa.Column('last_name', sa.String(length=35), nullable=True),
    sa.Column('email', sa.String(length=254), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('can_contact', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lead_email'), 'lead', ['email'], unique=True)
    op.create_index(op.f('ix_lead_phone_number'), 'lead', ['phone_number'], unique=True)
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content_id', sa.Integer(), nullable=True),
    sa.Column('cookie_uuid', sa.String(length=36), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    op.drop_index(op.f('ix_lead_phone_number'), table_name='lead')
    op.drop_index(op.f('ix_lead_email'), table_name='lead')
    op.drop_table('lead')
    op.drop_index(op.f('ix_content_slug'), table_name='content')
    op.drop_table('content')
    # ### end Alembic commands ###
