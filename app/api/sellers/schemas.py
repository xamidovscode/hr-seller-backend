from pydantic import BaseModel, Field

from app.models.choices import UserRoles


class SellerCreateSchema(BaseModel):
    username: str
    full_name: str
    password: str = Field(min_length=6, max_length=72)
    phone: str
    percentage: float
    duration: int


class SellersListSchema(BaseModel):
    id: int
    username: str
    full_name: str
    password: str
    phone: str
    is_active: bool
    role: str

