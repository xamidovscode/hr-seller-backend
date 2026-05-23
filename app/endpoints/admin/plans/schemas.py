from pydantic import BaseModel


class PlanUpdateSchema(BaseModel):
    id: int
    module: str
    trial_users: int
    min_users: int
    max_users: int
    price: int
    is_per_user: bool
    per_user_price: int
    is_active: bool


class PlanBulkUpdateSchema(BaseModel):
    plans: list[PlanUpdateSchema]

