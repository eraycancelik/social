"""foreign-key to posts table

Revision ID: 05d11939047c
Revises: 06177466e8c7
Create Date: 2023-11-13 14:29:14.957780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05d11939047c'
down_revision: Union[str, None] = '06177466e8c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.user_id"),nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["user_id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts","owner_id")
    pass
