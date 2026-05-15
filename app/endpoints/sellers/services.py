from typing import List, Any

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from app.models import users, choices, tenants, transactions
from app.resources import BaseService, TenantGrpcClient
from app.utils import hash_password
from . import schemas
from ...models.choices import TransTypes
from ...utils.time import now


class UserService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = TenantGrpcClient()

    async def create_user(self, schema: schemas.SellerCreateSchema) -> users.User:

        data = schema.model_copy(
            update={
                'password': hash_password(schema.password),
                'role': choices.UserRoles.seller
            }
        ).model_dump()
        supervisor_data = data.pop("supervisor", None)

        existing = await self.get_object_or_none(
            select(users.User).where(users.User.username == data['username'])
        )

        if existing:
            raise self.error("Bu username band!")

        async with self.atomic():
            seller = await self.save(model=users.User, **data)

            if supervisor_data:
                super_seller = await self.get_object_or_404(
                    select(users.User).where(users.User.id == supervisor_data['seller_id'])
                )

                await self.save(
                    model=users.Supervisor,
                    supervisor=super_seller,
                    seller=seller,
                    from_date=now().date(),
                    to_date=now().date() + relativedelta(months=supervisor_data['duration']),
                    percentage=supervisor_data['percentage'],
                )

        return seller

    async def sellers_list(self) -> List[dict[str, Any]]:

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

    async def seller_detail(self, seller_id: int) -> Any:

        seller = await self.get_object_or_404(
            select(users.User).where(users.User.id == seller_id)
        )

        assistants = await self.execute(
            select(
                users.Supervisor,
                func.coalesce(func.sum(transactions.SellerTransactions.amount), 0).label('income'),
            )
            .outerjoin(
                transactions.SellerTransactions,
                and_(
                    transactions.SellerTransactions.seller_id == users.Supervisor.seller_id,
                    transactions.SellerTransactions.month >= users.Supervisor.from_date,
                    transactions.SellerTransactions.month <= users.Supervisor.to_date,
                    transactions.SellerTransactions.type == TransTypes.INCOME
                )
            )
            .where(users.Supervisor.supervisor_id == seller_id)
            .group_by(users.Supervisor.id)
        )

        tenants_query = await self.execute(
            select(tenants.Tenant.core_tenant_id).where(tenants.Tenant.seller_id == seller_id)
        )

        tenants_data = await self._tenant_grpc.get_tenants_by_ids(ids=list(tenants_query.scalars().all()))

        assistants_data = [
            {
                'id': row.Supervisor.id,
                'seller_id': row.Supervisor.seller_id,
                'from_date': row.Supervisor.from_date,
                'to_date': row.Supervisor.to_date,
                'percentage': row.Supervisor.percentage,
                'amount_portion': row.income * (row.Supervisor.percentage / 100),
            }
            for row in assistants.mappings().all()
        ]

        return {
            'id': seller.id,
            'username': seller.username,
            'full_name': seller.full_name,
            'password': seller.password,
            'phone': seller.phone,
            'role': seller.role,
            'is_active': seller.is_active,
            'percentage': seller.percentage,
            'duration': seller.duration,
            'tenants': tenants_data,
            'assistants': assistants_data,
        }

user_service = UserService.annotated('db')


