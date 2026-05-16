import inspect
from typing import Annotated, Dict, Any, Type, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from ..mixins import SessionQueryMixin, HttpMixin
from app.resources.permissions.current_user import get_current_user
from app.models.users import User

T = TypeVar("T", bound="BaseService")

ARGS_TYPE: Dict[str, Any] = {
    "db": Annotated[AsyncSession, Depends(get_session)],
    "user": Annotated[User, Depends(get_current_user)],
}


class BaseService(SessionQueryMixin, HttpMixin):

    def __init__(self, db: AsyncSession = None, **kwargs):
        self.db: AsyncSession = db
        self._in_transaction: bool = False
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()

    @classmethod
    def __get_parameters(cls, fields: tuple):
        missing = [f for f in fields if f not in ARGS_TYPE]
        if missing:
            raise ValueError(
                f"ARGS_TYPE da aniqlanmagan fieldlar: {missing}. "
                f"Mavjud fieldlar: {list(ARGS_TYPE.keys())}"
            )
        return [
            inspect.Parameter(
                field,
                inspect.Parameter.KEYWORD_ONLY,
                annotation=ARGS_TYPE[field],
            )
            for field in fields
        ]

    @classmethod
    def __create_service(cls, *fields: str):
        fields = fields or ("db",)

        async def dynamic_method(**kwargs):
            return cls(**kwargs)

        sig = inspect.signature(dynamic_method).replace(
            parameters=cls.__get_parameters(fields)
        )
        dynamic_method.__signature__ = sig
        return dynamic_method

    @classmethod
    def annotated(cls: Type[T], *fields: str) -> Type[Annotated[T, Depends]]:
        """
        Dependency injection uchun annotated tip qaytaradi.

        Misol (faqat DB):
            user_service = UserService.annotated()

        Misol (DB + Redis):
            cache_service = CacheService.annotated("db", "redis")

        Misol (DB + current_user):
            profile_service = ProfileService.annotated("db", "current_user")
        """
        return Annotated[cls, Depends(cls.__create_service(*fields))]