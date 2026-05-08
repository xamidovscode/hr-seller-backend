__all__ = (
    'SellerTransactions',
)

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, ForeignKey, String, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import BaseModel

if TYPE_CHECKING:
    from app.models import User, MonthlyTransaction


class SellerTransactions(BaseModel):
    __tablename__ = 'seller_transactions'

    seller_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    seller: Mapped['User'] = relationship(
        back_populates='seller_transactions'
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(36, 2),
        default=Decimal('0.00'),
        server_default='0.00',
        comment="Amount of transaction",
    )
    model: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Balance model",
    )
    instance_id: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default='0',
        comment="Instance ID",
    )

    type: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default='1',
        comment="Transaction type",
    )

    tenant_monthly_transactions: Mapped[list['MonthlyTransaction']] = relationship(
        back_populates="seller_trans",
    )

    __table_args__ = (
        CheckConstraint('type IN (1, -1)'),
    )

