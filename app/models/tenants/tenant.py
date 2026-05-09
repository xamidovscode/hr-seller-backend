__all__ = (
    'Tenant',
)

from typing import TYPE_CHECKING

from datetime import date
from decimal import Decimal

from sqlalchemy import Integer, Enum as SQLEnum, Date, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import BaseModel
from .. import choices


if TYPE_CHECKING:
    from app.models import User, MonthlyTransaction


class Tenant(BaseModel):
    __tablename__ = "tenants"

    tenant_id: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="Tenant id: in core service!",
    )
    type: Mapped[choices.TenantTypes] = mapped_column(
        SQLEnum(choices.TenantTypes),
        default=choices.TenantTypes.IMB_HR,
        nullable=False,
        comment="The type of the tenant",
    )
    from_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="The start date of the tenant",
    )
    to_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="The end date of the tenant",
    )
    percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        comment="The percentage of the tenant",
    )

    seller_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    seller: Mapped['User'] = relationship(
        back_populates="tenants",
    )

    monthly_transactions: Mapped[list['MonthlyTransaction']] = relationship(
        back_populates="tenant",
    )



