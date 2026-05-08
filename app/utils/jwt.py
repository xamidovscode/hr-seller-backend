__all__ = (
    'hash_password',
    'verify_password',
    'decode_access_token',
    'create_access_token',
)

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from jwt import InvalidTokenError
from fastapi import HTTPException, status
from app.core.settings import settings
from app.models import users

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: users.User) -> str:
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    print(payload, settings.SECRET_KEY, settings.ALGORITHM)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token talab qilinadi"
            )

        return payload

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz yoki muddati tugagan"
        )

