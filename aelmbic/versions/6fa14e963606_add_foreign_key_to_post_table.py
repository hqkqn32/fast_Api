"""add foreign key to post table

Revision ID: 6fa14e963606
Revises: f2f24aa84acc
Create Date: 2024-12-19 13:57:48.790390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fa14e963606'
down_revision: Union[str, None] = 'f2f24aa84acc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(), nullable=False))
    op.create_foreign_key("posts_user_fk",source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_user_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
