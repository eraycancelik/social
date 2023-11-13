"""create posts table

Revision ID: 6d2c18cbf3e7
Revises: 
Create Date: 2023-11-13 14:16:37.609872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d2c18cbf3e7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
        sa.Column("post_id",sa.Integer(),primary_key=True,nullable=False),
        sa.Column("title",sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
