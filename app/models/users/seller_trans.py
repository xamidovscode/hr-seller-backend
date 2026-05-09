__all__ = (
    'SellerTransactions',
)

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Numeric,
    ForeignKey,
    String,
    Integer,
    Enum as SQLEnum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.db import BaseModel
from .. import choices

if TYPE_CHECKING:
    from app.models import User, MonthlyTransaction, SellerRequest


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

    type: Mapped[choices.TransTypes] = mapped_column(
        SQLEnum(choices.TransTypes)
    )

    tenant_monthly_transactions: Mapped[list['MonthlyTransaction']] = relationship(
        back_populates="seller_trans",
    )
    seller_requests: Mapped[list['SellerRequest']] = relationship(
        back_populates="seller_transaction",
    )


