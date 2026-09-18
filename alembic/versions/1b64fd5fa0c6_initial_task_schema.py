"""initial task schema

Revision ID: 1b64fd5fa0c6
Revises:
Create Date: 2026-09-17 12:23:35.710896

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1b64fd5fa0c6"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("priority", sa.String(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.UniqueConstraint("task_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tasks")
