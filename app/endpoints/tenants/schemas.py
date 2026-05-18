from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class TenantCreateSchema(BaseModel):
    domain: str
    name: str
    seller_id: Optional[int] = None


class TenantUpdateSchema(BaseModel):
    is_active: bool


class MonthlyTransactionCreateSchema(BaseModel):
    tenant_id: int
    month: date
    amount: Decimal = Field(default=Decimal("0.00"), ge=0)


class MonthlyTransactionUpdateSchema(BaseModel):
    service_id: Optional[int] = None
    month: Optional[date] = None
    amount: Optional[Decimal] = Field(default=None, ge=0)
