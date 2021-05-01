"""created DataSource and Feedback models

Revision ID: ecc1b8f4deb3
Revises: 
Create Date: 2020-05-16 23:16:10.025893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecc1b8f4deb3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dataSource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fileName', sa.String(length=45), nullable=False),
    sa.Column('dateUploaded', sa.DateTime(), nullable=True),
    sa.Column('fileDescription', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fileName')
    )
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customerName', sa.String(length=80), nullable=False),
    sa.Column('feedbackInformation', sa.Text(), nullable=True),
    sa.Column('feedbackDate', sa.DateTime(), nullable=True),
    sa.Column('feedbackType', sa.String(length=10), nullable=True),
    sa.Column('datasrc_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['datasrc_id'], ['dataSource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    op.drop_table('dataSource')
    # ### end Alembic commands ###
