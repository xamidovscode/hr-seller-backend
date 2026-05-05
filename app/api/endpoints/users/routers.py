from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.get_session import get_session
from app.models import users
from . import schemas

router = APIRouter(prefix="/users", tags=["users"])


@router.post('/create/', response_model=schemas.UsersListSchema)
async def create_user(
        body: schemas.UserCreateSchema, session: AsyncSession = Depends(get_session),
):
    existing_user = await session.execute(select(users.User).where(users.User.username == body.username))

    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Bu username band!")

    user = users.User(
        username=body.username,
        full_name=body.full_name,
        password=hash_password(body.password),
        phone=body.phone,
        is_active=True,
        role=body.role,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get('/list/', response_model=List[schemas.UsersListSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(users.User))
    queryset = result.scalars().all()
    return queryset





