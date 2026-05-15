from typing import List, Any

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from app.models import users, choices, tenants, transactions
from app.resources import BaseService, TenantGrpcClient
from app.utils import hash_password
from . import schemas
from ...models.choices import TransTypes
from ...resources.seller.seller_balance_calculator import SellerBalanceCalculator
from ...utils.time import now


class UserService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = TenantGrpcClient()

    async def sellers_list(self) -> List[dict[str, Any]]:
        sellers = await self.get_all(
            select(users.User).where(users.User.role == choices.UserRoles.seller)
        )

        calc = SellerBalanceCalculator(self.db)
        stats = await calc.bulk_breakdown([s.id for s in sellers])

        return [
            {
                'id': s.id,
                'username': s.username,
                'full_name': s.full_name,
                'phone': s.phone,
                'percentage': s.percentage,
                'duration': s.duration,
                'is_active': s.is_active,
                **stats[s.id],
            }
            for s in sellers
        ]

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

    async def seller_detail(self, seller_id: int) -> Any:

        seller = await self.get_object_or_404(
            select(users.User).where(users.User.id == seller_id)
        )

        assistants = await self.execute(
            select(
                users.Supervisor,
                func.coalesce(func.sum(transactions.SellerTransactions.amount), 0).label('income'),
            )
            .options(selectinload(users.Supervisor.seller))
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

        assistants_data = [
            {
                'id': row.Supervisor.id,
                'seller_id': row.Supervisor.seller_id,
                'from_date': row.Supervisor.from_date,
                'to_date': row.Supervisor.to_date,
                'percentage': row.Supervisor.percentage,
                'amount_portion': row.income * (row.Supervisor.percentage / 100),
                'full_name': row.Supervisor.seller.full_name,
            }
            for row in assistants.mappings().all()
        ]

        tenants_query = await self.execute(
            select(tenants.Tenant.core_tenant_id)
            .where(tenants.Tenant.seller_id == seller_id)
        )
        tenants_data = await self._tenant_grpc.get_tenants_by_ids(ids=list(tenants_query.scalars().all()))

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
            'assistants': assistants_data,
            'tenants': tenants_data,
        }

user_service = UserService.annotated('db')


