"""contact_message table.

Revision ID: contact0001
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "contact0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "contact_message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("read", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_contact_message_read"), "contact_message", ["read"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_contact_message_read"), table_name="contact_message")
    op.drop_table("contact_message")
