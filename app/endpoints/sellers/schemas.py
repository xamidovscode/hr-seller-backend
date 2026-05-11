from pydantic import BaseModel, Field
from app.resources.fields import UsernameField


class SellerCreateSchema(BaseModel):
    username: UsernameField
    full_name: str
    password: str = Field(min_length=6, max_length=72)
    phone: str
    percentage: float
    duration: int


class SellerCreateResponseSchema(BaseModel):
    id: int
    username: str
    full_name: str
    phone: str
    is_active: bool
    role: str
    seller_count: int


