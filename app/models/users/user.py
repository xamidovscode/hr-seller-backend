__all__ =(
    'User',
    'Supervisor',
)

from datetime import date as date_field
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Enum as SQLEnum,
    Numeric, ForeignKey, Date,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.db import BaseModel
from app.models.choices import UserRoles

if TYPE_CHECKING:
    from app.models import (
        Tenant,
        SellerTransactions,
    )


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        comment="Username",
    )
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="User's full name",
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="User's password",
    )
    phone: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="User's phone number",
    )
    role: Mapped[UserRoles] = mapped_column(
        SQLEnum(UserRoles),
        default=UserRoles.seller,
        server_default='seller',
        nullable=False,
        comment="User's role",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether the user is active",
    )
    percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        default=0,
        nullable=False,
        comment="User's percentage",
    )
    duration: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="The duration of the user",
    )

    tenants: Mapped[list['Tenant']] = relationship(
        back_populates="seller",
    )
    seller_transactions: Mapped[list['SellerTransactions']] = relationship(
        back_populates="seller",
    )

    supervised_sellers: Mapped[list['Supervisor']] = relationship(
        foreign_keys="Supervisor.supervisor_id",
        back_populates="supervisor",
    )
    my_supervisors: Mapped[list['Supervisor']] = relationship(
        foreign_keys="Supervisor.seller_id",
        back_populates="seller",
    )


class Supervisor(BaseModel):
    __tablename__ = "supervisors"

    supervisor_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    seller_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )

    supervisor: Mapped[User] = relationship(
        foreign_keys=[supervisor_id],
        back_populates="supervised_sellers",
    )
    seller: Mapped[User] = relationship(
        foreign_keys=[seller_id],
        back_populates="my_supervisors",
    )

    from_date: Mapped[date_field] = mapped_column(
        Date,
        nullable=False,
        comment="The start date of the supervisor deadline",
    )
    to_date: Mapped[date_field] = mapped_column(
        Date,
        nullable=False,
        comment="The end date of the supervisor deadline",
    )
    percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        default=0,
        nullable=False,
        comment="The percentage of the supervisor deadline",
    )



