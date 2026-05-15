from typing import Optional

from pydantic import BaseModel


class TenantCreateSchema(BaseModel):
    domain: str
    name: str
    seller_id: Optional[int] = None


class TenantUpdateSchema(BaseModel):
    is_active: bool
