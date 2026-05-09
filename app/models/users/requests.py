__all__ = (
    'SellerRequest',
)

from datetime import date as date_field
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.db import BaseModel
from .. import choices

if TYPE_CHECKING:
    from app.models import User, SellerTransactions


class SellerRequest(BaseModel):
    __tablename__ = "seller_requests"

    seller_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    seller: Mapped['User'] = relationship(
        back_populates="seller_requests",
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(36, 2),
        default=0,
        server_default='0',
        comment="The amount of the seller request",
    )
    date: Mapped[date_field] = mapped_column(
        Date,
        nullable=False,
        comment="The date of the seller request",
    )
    condition: Mapped[choices.RequestConditions] = mapped_column(
        SQLEnum(choices.RequestConditions),
        default=choices.RequestConditions.PENDING,
        comment="The condition of the seller request",
    )

    seller_transaction_id: Mapped[int] = mapped_column(
        ForeignKey("seller_transactions.id", ondelete="CASCADE"),
    )
    seller_transaction: Mapped['SellerTransactions'] = relationship(
        back_populates="seller_transactions",
    )

