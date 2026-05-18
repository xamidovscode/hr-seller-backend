from typing import Optional

from pydantic import BaseModel, Field
from app.resources.fields import (
    UsernameField,
    PercentageField,
    PositiveIntField,
)



class SupervisorCreateSchema(BaseModel):
    seller_id: PositiveIntField
    percentage: PercentageField
    duration: PositiveIntField


class SellerCreateSchema(BaseModel):
    username: UsernameField
    full_name: str
    password: str = Field(min_length=6, max_length=72)
    phone: str
    percentage: float
    duration: int
    supervisor: Optional[SupervisorCreateSchema] = None


class SellerUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    percentage: Optional[float] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None


class SellerCreateResponseSchema(BaseModel):
    id: int
    username: str
    full_name: str
    phone: str
    is_active: bool
    role: str


