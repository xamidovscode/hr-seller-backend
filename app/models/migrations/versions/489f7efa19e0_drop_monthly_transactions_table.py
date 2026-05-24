"""drop_monthly_transactions_table

Revision ID: 489f7efa19e0
Revises: f9dccb8c6b28
Create Date: 2026-05-24 10:56:02.599097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '489f7efa19e0'
down_revision: Union[str, Sequence[str], None] = 'f9dccb8c6b28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('tenant_monthly_transactions')


def downgrade() -> None:
    op.create_table(
        'tenant_monthly_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('service_id', sa.Integer(), nullable=False, comment='Core service, MonthlyTransaction ID'),
        sa.Column('month', sa.Date(), nullable=False, comment='Month: format YEAR-MONTH-01'),
        sa.Column('amount', sa.Numeric(36, 2), server_default='0.00', nullable=True, comment='Month: amount of monthly transaction'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )