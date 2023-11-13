"""create address table

Revision ID: ea08f01d3900
Revises: e1bed8f8e5c3
Create Date: 2023-11-13 16:18:47.244455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea08f01d3900'
down_revision: Union[str, None] = 'e1bed8f8e5c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("addresses",
        sa.Column("address_id",sa.Integer,primary_key=True,nullable=False),
        sa.Column("address_type",sa.String,nullable=False),
        sa.Column("address_user_name",sa.String,nullable=False),
        sa.Column("address_user_surname",sa.String,nullable=False),
        sa.Column("address_user_phone",sa.String,nullable=False),
        sa.Column("address_city",sa.String,nullable=False),
        sa.Column("address_line",sa.String,nullable=False),
        sa.Column("zipcode",sa.Integer,nullable=False),
        sa.Column("customer_id",sa.Integer,sa.ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False),
        sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_table("addresses")
    pass
