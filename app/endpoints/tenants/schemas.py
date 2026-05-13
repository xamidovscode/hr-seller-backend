from pydantic import BaseModel


class TenantCreateSchema(BaseModel):
    success: bool

