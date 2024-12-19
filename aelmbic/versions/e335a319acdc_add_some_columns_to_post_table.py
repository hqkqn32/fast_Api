"""add some columns to post table

Revision ID: e335a319acdc
Revises: 6fa14e963606
Create Date: 2024-12-19 14:07:51.503641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e335a319acdc'
down_revision: Union[str, None] = '6fa14e963606'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="True"))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column("posts",column_name="published")
    op.drop_column(table_name="posts",column_name="created_At")
    pass


