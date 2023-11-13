"""add user table

Revision ID: 06177466e8c7
Revises: b34b2547e912
Create Date: 2023-11-13 14:21:59.940013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06177466e8c7'
down_revision: Union[str, None] = 'b34b2547e912'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
        sa.Column("user_id",sa.Integer(),nullable=False),
        sa.Column("name",sa.String,nullable=False),
        sa.Column("surname",sa.String,nullable=False),
        sa.Column("email",sa.String,nullable=False,unique=True),
        sa.Column("password",sa.String,nullable=False),
        sa.Column("phone",sa.Text,nullable=False,unique=True),
        sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("user_id"))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
