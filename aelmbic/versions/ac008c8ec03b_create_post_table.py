"""create post table

Revision ID: ac008c8ec03b
Revises: 
Create Date: 2024-12-18 11:59:04.074150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac008c8ec03b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",sa.Column("id",sa.Integer(),nullable=True,primary_key=True),sa.Column("title",sa.VARCHAR(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
