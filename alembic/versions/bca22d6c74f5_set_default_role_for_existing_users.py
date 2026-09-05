"""set default role for existing users

Revision ID: bca22d6c74f5
Revises: fc5ce9a539ac
Create Date: 2026-09-05 18:57:21.442542

"""
from typing import Sequence, Union

from alembic import op



# revision identifiers, used by Alembic.
revision: str = 'bca22d6c74f5'
down_revision: Union[str, Sequence[str], None] = 'fc5ce9a539ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL ")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE users SET role = NULL WHERE role = 'user'")
