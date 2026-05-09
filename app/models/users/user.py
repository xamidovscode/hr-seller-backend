__all__ =(
    'User',
)

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Enum as SQLEnum,
    Numeric,
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
        SellerRequest,
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
    seller_requests: Mapped[list['SellerRequest']] = relationship(
        back_populates="seller",
    )





