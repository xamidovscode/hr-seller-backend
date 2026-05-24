from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.models.choices import RequestConditions


class SellerRequestCreateSchema(BaseModel):
    seller_id: int
    amount: Decimal
    date: date
    condition: RequestConditions = RequestConditions.PENDING


class SellerRequestUpdateSchema(BaseModel):
    amount: Decimal
    date: date
    condition: RequestConditions


class SellerRequestFilterSchema(BaseModel):
    seller_id: Optional[int] = None
    condition: Optional[RequestConditions] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
