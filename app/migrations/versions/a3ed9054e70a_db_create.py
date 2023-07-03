"""DB create

Revision ID: a3ed9054e70a
Revises: 
Create Date: 2023-07-03 15:11:49.261063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3ed9054e70a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("is_superuser", sa.Boolean(), default=False, nullable=False),
        sa.Column("is_verified", sa.Boolean(), default=False, nullable=False)
    )
    op.create_table(
        "workplace",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("key", sa.String(), nullable=False)
    )
    op.create_table(
        "post",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String()),
        sa.Column(
            "workplace_id",
            sa.Integer,
            sa.ForeignKey("workplace.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("date_create", sa.TIMESTAMP, nullable=False)
    )


def downgrade():
    op.drop_table("user")
    op.drop_table("workplace")
    op.drop_table("post")
