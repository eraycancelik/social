"""creating products table

Revision ID: e1bed8f8e5c3
Revises: 41e797746e11
Create Date: 2023-11-13 16:15:01.139704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1bed8f8e5c3'
down_revision: Union[str, None] = '41e797746e11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("products",
        sa.Column("product_id",sa.Integer,primary_key=True,index=True,nullable=False),
        sa.Column("product_name",sa.String,index=True,nullable=False),
        sa.Column("product_category",sa.String,nullable=False),
        sa.Column("product_price",sa.Integer,nullable=False),
        sa.Column("product_photo_url",sa.String,nullable=False),
        sa.Column("inventory",sa.Integer,server_default="100",nullable=False),
        sa.Column("is_sale",sa.Boolean,server_default='True',nullable=False),
        sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_table("products")
    pass
