"""alter_core_tenant_id

Revision ID: a70ae5e599b0
Revises: 1370d17a0c4b
Create Date: 2026-05-14 15:53:17.666852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a70ae5e599b0'
down_revision: Union[str, Sequence[str], None] = '1370d17a0c4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('tenants', 'tenant_id', new_column_name='core_tenant_id')


def downgrade() -> None:
    op.alter_column('tenants', 'core_tenant_id', new_column_name='tenant_id')
