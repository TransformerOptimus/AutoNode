"""create_requests_table

Revision ID: 22bd93a20597
Revises: 
Create Date: 2024-05-17 17:19:52.440335

"""
from typing import Sequence, Union
from autonode.utils.enums.request_status import RequestStatus
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22bd93a20597'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'requests',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('url', sa.String, nullable=False),
        sa.Column('requests_dir', sa.String, nullable=False),
        sa.Column('tree_location', sa.String, nullable=False),
        sa.Column('status', sa.String, nullable=False, default=RequestStatus.PENDING.value),
        sa.Column('completed_at', sa.DateTime, default=None),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('is_deleted', sa.Boolean, nullable=False, default=sa.false(), server_default=sa.text('false'))
    )


def downgrade():
    op.drop_table('requests')
