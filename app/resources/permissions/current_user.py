from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import decode_access_token
from app.core.db import get_session
from app.models import users

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    user = await session.get(users.User, int(user_id))

    if not user:
        raise HTTPException(status_code=401, detail="User topilmadi")

    return user