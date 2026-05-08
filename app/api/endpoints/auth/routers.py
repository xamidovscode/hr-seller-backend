from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import verify_password, create_access_token
from app.core.db import get_session
from app.models import users
from app.resources.permissions.current_user import get_current_user
from . import schemas


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
        body: schemas.LoginSchema, session: AsyncSession = Depends(get_session)
):
    users_query = await session.execute(
        select(users.User)
        .where(
            users.User.is_active == True,
            users.User.username == body.username,
        )
    )
    user = users_query.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Foydalanuvchi topilmadi!")

    if not verify_password(plain_password=body.password, hashed_password=user.password):
        raise HTTPException(status_code=400, detail="Xato parol kiritildi!")

    return {
        'user_id': user.id,
        'username': user.username,
        'full_name': user.full_name,
        'phone': user.phone,
        'is_active': user.is_active,
        'access_token': create_access_token(user),
    }



@router.get("/profile")
async def get_profile(user: users.User = Depends(get_current_user)):
    return {
        'user_id': user.id,
        'username': user.username,
        'full_name': user.full_name,
        'phone': user.phone,
        'is_active': user.is_active,
        'role': user.role,
    }