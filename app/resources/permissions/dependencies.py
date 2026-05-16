from fastapi import Depends, HTTPException, status

from app.models.choices import UserRoles
from app.models.users import User
from app.resources.permissions.current_user import get_current_user


def require_roles(*roles: UserRoles):
    allowed = frozenset(roles)

    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="Sizning rolingiz bu amalga ruxsat bermaydi",
            )
        return user

    return checker