from collections import defaultdict
from typing import List, Any

from fastapi import status
from sqlalchemy import select, func
from sqlalchemy.orm import aliased, selectinload

from app.models import users, choices, tenants, User, Supervisor
from app.resources import BaseService
from app.utils import hash_password
from . import schemas
from ...models.choices import UserRoles


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
                tenants_count_sq.c.tenant_count,
            )
            .outerjoin(
                tenants_count_sq,
                tenants_count_sq.c.seller_id == users.User.id
            )
            .where(
                users.User.role == choices.UserRoles.seller
            )
            .options(
                selectinload(users.User.supervised_sellers).selectinload(users.Supervisor.seller)
            )
        )

        sellers = await self.execute(stmt)
        result = []

        for user, tenant_count in sellers.unique().all():
            supervised_list = []
            for supervisor_record in user.supervised_sellers:
                supervised_list.append({
                    "supervisor_record_id": supervisor_record.id,
                    "seller_id": supervisor_record.seller_id,
                    "seller_username": supervisor_record.seller.username,
                    "seller_full_name": supervisor_record.seller.full_name,
                    "seller_phone": supervisor_record.seller.phone,
                    "seller_is_active": supervisor_record.seller.is_active,
                    "seller_percentage": supervisor_record.seller.percentage,
                    "seller_duration": supervisor_record.seller.duration,
                    "from_date": supervisor_record.from_date,
                    "to_date": supervisor_record.to_date,
                    "percentage": supervisor_record.percentage,
                })

            result.append({
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "phone": user.phone,
                "role": user.role,
                "is_active": user.is_active,
                "percentage": user.percentage,
                "duration": user.duration,
                "tenant_count": tenant_count or 0,
                "seller_count": len(supervised_list),
                "supervised_sellers": supervised_list,
                'balance': 0
            })

        return result

user_service = UserService.annotated('db')


