__all__ = (
    'MonthlyTransaction',
)

from decimal import Decimal
from datetime import date as date_field
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import BaseModel

if TYPE_CHECKING:
    from app.models import Tenant, SellerTransactions


class MonthlyTransaction(BaseModel):
    __tablename__ = "tenant_monthly_transactions"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('tenants.id', ondelete="CASCADE"),
    )
    tenant: Mapped['Tenant'] = relationship(
        back_populates="monthly_transactions",
    )
    service_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Core service, MonthlyTransaction ID",
    )
    month: Mapped[date_field] = mapped_column(
        Date,
        nullable=False,
        comment="Month: format YEAR-MONTH-01",
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(36, 2),
        default=Decimal("0.00"),
        server_default='0.00',
        comment="Month: amount of monthly transaction",
    )

    seller_trans_id: Mapped[int] = mapped_column(
        ForeignKey('seller_transactions.id', ondelete="CASCADE"),
        nullable=False,
    )
    seller_trans: Mapped['SellerTransactions'] = relationship(
        back_populates="tenant_monthly_transactions",
    )

