from collections import defaultdict
from typing import List, Any

from fastapi import status
from sqlalchemy import select, func

from app.models import users, choices, tenants, Supervisor, User
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

    async def get_sellers_count_by_supervisor(self) -> List[dict[str, Any]]:

        stmt = (
            select(
                users.Supervisor.id.label("supervisor_id"),
                Supervisor.username.label("username"),
                Supervisor.full_name.label("full_name"),

                users.Supervisor.id.label("relation_id"),

                User.id.label("seller_id"),
                Us.username.label("seller_username"),

                users.Supervisor.from_date,
                users.Supervisor.to_date,
                users.Supervisor.percentage,
            )
            .select_from(SupervisorUser)
            .outerjoin(
                users.Supervisor,
                users.Supervisor.supervisor_id == SupervisorUser.id
            )
            .outerjoin(
                SellerUser,
                users.Supervisor.seller_id == SellerUser.id
            )
            .where(
                SupervisorUser.role == choices.UserRoles.supervisor
            )
        )

        result = await self.execute(stmt)

        data = defaultdict(lambda: {
            "id": None,
            "username": None,
            "full_name": None,
            "seller_count": 0,
            "tenant_count": 0,
            "sellers": []
        })

        for row in result.all():
            sup_id = row.supervisor_id

            # initialize supervisor
            if data[sup_id]["id"] is None:
                data[sup_id]["id"] = row.supervisor_id
                data[sup_id]["username"] = row.username
                data[sup_id]["full_name"] = row.full_name

            # agar seller bo‘lsa
            if row.seller_id is not None:
                data[sup_id]["sellers"].append({
                    "id": row.seller_id,
                    "username": row.seller_username,
                    "from_date": row.from_date,
                    "to_date": row.to_date,
                    "percentage": row.percentage,
                })

                data[sup_id]["seller_count"] += 1

        return list(data.values())

user_service = UserService.annotated('db')


