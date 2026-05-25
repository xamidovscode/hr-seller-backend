from datetime import date
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field


class TenantPlansCreateSchema(BaseModel):
    module: int
    users_count: int


class TenantCreateSchema(BaseModel):
    domain: str
    name: str
    deadline: date
    plans: Optional[List[TenantPlansCreateSchema]] = None
    personal_amount: Decimal = Field(default=Decimal("0"), max_digits=36, decimal_places=2)
    seller_id: Optional[int] = None


class TenantUpdateSchema(BaseModel):
    is_active: bool
    on_trial: bool
    is_deleted: bool
    deadline: date


class ActivePlanItemSchema(BaseModel):
    users_count: int
    is_active: bool
    module: str


class ActivePlanUpdateSchema(BaseModel):
    plans: List[ActivePlanItemSchema]



