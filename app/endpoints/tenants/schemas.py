from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.choices import TenantTypes


class TenantCreateSchema(BaseModel):
    domain: str
    name: str
    seller_id: Optional[int] = None


