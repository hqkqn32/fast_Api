"""add content on posts 

Revision ID: 40382f1db9b9
Revises: ac008c8ec03b
Create Date: 2024-12-18 12:49:37.901944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40382f1db9b9'
down_revision: Union[str, None] = 'ac008c8ec03b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
     pass 
    
    


def downgrade() -> None:
    op.drop_column("posts","content")
    pass

