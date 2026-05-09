from fastapi import status
from sqlalchemy import select

from app.models import users, choices
from app.resources import BaseService
from app.utils import hash_password
from . import schemas


class UserService(BaseService):

    async def create_user(self, schema: schemas.SellerCreateSchema) -> users.User:

        existing = await self.get_object_or_none(
            select(users.User).where(users.User.username == schema.username)
        )

        if existing:
            raise self.error("Bu username band!", status.HTTP_400_BAD_REQUEST)

        return await self.save(
            model=users.User,
            schema=schema.model_copy(
                update={
                    'password': hash_password(schema.password),
                    'role': choices.UserRoles.seller
                }
            ),
        )


user_service = UserService.annotated('db')

