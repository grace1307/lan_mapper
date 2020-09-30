"""empty message

Revision ID: 68676dcadcb2
Revises:

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68676dcadcb2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('detected_device',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mac_addr', sa.String(length=50), nullable=True),
    sa.Column('last_ip', sa.String(length=50), nullable=True),
    sa.Column('vendor', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_detected_device')),
    sa.UniqueConstraint('mac_addr', name=op.f('uq_detected_device_mac_addr')),
    mysql_charset='utf8',
    mysql_collate='utf8_general_ci',
    mysql_engine='InnoDB'
    )
    op.create_table('detection_record',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('runtime', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_detection_record')),
    mysql_charset='utf8',
    mysql_collate='utf8_general_ci',
    mysql_engine='InnoDB'
    )
    op.create_table('known_device',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mac_addr', sa.String(length=50), nullable=False),
    sa.Column('owner', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('vendor', sa.String(length=200), nullable=True),
    sa.Column('model', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_known_device')),
    sa.UniqueConstraint('mac_addr', name=op.f('uq_known_device_mac_addr')),
    mysql_charset='utf8',
    mysql_collate='utf8_general_ci',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('known_device')
    op.drop_table('detection_record')
    op.drop_table('detected_device')
    # ### end Alembic commands ###