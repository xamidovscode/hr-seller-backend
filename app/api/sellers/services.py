from typing import List, Any

from fastapi import status
from sqlalchemy import select, func

from app.models import users, choices, tenants
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

        seller_count_sq = (
            select(
                users.Supervisor.supervisor_id.label('supervisor_id'),
                func.count(users.Supervisor.id).label('seller_count')
            )
            .group_by(users.Supervisor.supervisor_id)
        ).subquery()

        tenants_count_sq = (
            select(
                tenants.Tenant.seller_id.label('seller_id'),
                func.count(tenants.Tenant.id).label('tenant_count')
            )
            .group_by(tenants.Tenant.seller_id)
        ).subquery()

        stmt = (
            select(
                users.User,
                seller_count_sq.c.seller_count,
                tenants_count_sq.c.tenant_count,
            )
            .outerjoin(
                seller_count_sq,
                seller_count_sq.c.supervisor_id == users.User.id
            )
            .outerjoin(
                tenants_count_sq,
                tenants_count_sq.c.seller_id == users.User.id
            )
            .where(
                users.User.role == choices.UserRoles.seller
            )
        )

        result = await self.execute(stmt)

        return [
            {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "phone": user.phone,
                "role": user.role,
                "is_active": user.is_active,
                "percentage": user.percentage,
                "duration": user.duration,
                "seller_count": seller_count or 0,
                "tenant_count": tenant_count or 0,
            }
            for user, seller_count, tenant_count in result.all()
        ]

user_service = UserService.annotated('db')


