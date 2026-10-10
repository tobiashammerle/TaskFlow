"""add owner id to tasks

Revision ID: 23e2dc6e96ca
Revises: 6aace9b7e79a
Create Date: 2026-10-09 07:10:53.535525

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "23e2dc6e96ca"
down_revision: Union[str, Sequence[str], None] = "6aace9b7e79a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Uuid(), nullable=False))
        batch_op.create_foreign_key(
            "fk_tasks_owner_id_users", "users", ["owner_id"], ["user_id"]
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_constraint("fk_tasks_owner_id_users", type_="foreignkey")
        batch_op.drop_column("owner_id")
