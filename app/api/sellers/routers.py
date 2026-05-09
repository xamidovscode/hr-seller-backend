from typing import List

from fastapi import APIRouter
from sqlalchemy import select

from app.models import users, choices
from . import schemas
from .services import user_service

router = APIRouter(prefix="/sellers", tags=["sellers"])


@router.post('/create/', response_model=schemas.SellersListSchema)
async def seller_user(schema: schemas.SellerCreateSchema, service: user_service):
    return await service.create_user(schema)


@router.get('/list/', response_model=List[schemas.SellersListSchema])
async def get_all_sellers(service: user_service):
    return await service.get_all(
        select(users.User).where(
            users.User.is_active == True, users.User.role == choices.UserRoles.seller
        )
    )

