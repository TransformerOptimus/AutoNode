"""create_files_table

Revision ID: 9249a4e23a07
Revises: 22bd93a20597
Create Date: 2024-05-17 17:19:57.860295

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import JSONB
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9249a4e23a07'
down_revision: Union[str, None] = '22bd93a20597'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'files',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('request_id', sa.INTEGER, nullable=False),
        sa.Column('path', sa.String, nullable=False),
        sa.Column('category', sa.String, nullable=True),
        sa.Column('meta_data', JSONB, nullable=True),
        sa.Column('file_type', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('is_deleted', sa.Boolean, nullable=False, default=sa.false(), server_default=sa.text('false'))
    )


def downgrade():
    op.drop_table('files')
