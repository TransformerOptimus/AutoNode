"""create_actions_table

Revision ID: 6f5f151a425f
Revises: 9249a4e23a07
Create Date: 2024-05-17 17:20:02.119038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f5f151a425f'
down_revision: Union[str, None] = '9249a4e23a07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'actions',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('request_id', sa.INTEGER, nullable=False),
        sa.Column('screenshot_id', sa.INTEGER, nullable=True),
        sa.Column('prompt', sa.String, nullable=False),
        sa.Column('llm_response', sa.String, nullable=False),
        sa.Column('action', sa.String, nullable=False),
        sa.Column('node_id', sa.INTEGER, nullable=False),
        sa.Column('text', sa.String, default=""),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('is_deleted', sa.Boolean, nullable=False, default=sa.false(), server_default=sa.text('false'))
    )

def downgrade():
    op.drop_table('actions')
