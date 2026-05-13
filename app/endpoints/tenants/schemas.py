from pydantic import BaseModel


class TenantCreateSchema(BaseModel):
    domain: str
    name: str



