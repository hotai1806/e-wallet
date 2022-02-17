"""empty message

Revision ID: c7eecf77fbe3
Revises: 6bb9fd2b2fac
Create Date: 2022-02-13 21:05:34.898990

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c7eecf77fbe3"
down_revision = "6bb9fd2b2fac"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "merchants", sa.Column("api_key", postgresql.UUID(as_uuid=True), nullable=False)
    )
    op.drop_column("merchants", "apiKey")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "merchants",
        sa.Column("apiKey", postgresql.UUID(), autoincrement=False, nullable=False),
    )
    op.drop_column("merchants", "api_key")
    # ### end Alembic commands ###
