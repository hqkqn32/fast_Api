"""add user table 

Revision ID: f2f24aa84acc
Revises: 40382f1db9b9
Create Date: 2024-12-19 13:27:51.226884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2f24aa84acc'
down_revision: Union[str, None] = '40382f1db9b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer,nullable=False),
                    sa.Column("email",sa.String,nullable=False),
                    sa.Column("password",sa.String,nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
