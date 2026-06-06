"""initial migrate

Revision ID: d22a204ac0ac
Revises: 
Create Date: 2026-06-06 01:35:48.333075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd22a204ac0ac'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
