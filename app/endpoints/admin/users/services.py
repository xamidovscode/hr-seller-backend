from decimal import Decimal
from typing import List, Any

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, func

from app.core.settings import settings
from app.models import (
    choices,
    User,
    Supervisor,
    Tenant,
    SellerRequest,
)
from app.resources import BaseService, TenantGrpcClient
from app.resources.seller.seller_balance_calculator import SellerBalanceCalculator
from app.utils import hash_password
from app.utils.time import now
from . import schemas

_tenant_grpc = TenantGrpcClient()


class UserService(BaseService):

    async def sellers_list(self) -> List[dict[str, Any]]:
        sellers = await self.get_all(
            select(User)
            .where(
                User.role == choices.UserRoles.seller,
                User.is_active == True,
            )
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

    async def create_seller(self, schema: schemas.SellerCreateSchema) -> User:

        data = schema.model_copy(
            update={
                'password': hash_password(schema.password),
                'role': choices.UserRoles.seller
            }
        ).model_dump()
        supervisor_data = data.pop("supervisor", None)

        existing = await self.get_object_or_none(
            select(User).where(User.username == data['username'])
        )

        if existing:
            raise self.error("Bu username band!")

        async with self.atomic():
            seller = await self.save(model=User, **data)

            if supervisor_data:
                super_seller = await self.get_object_or_404(
                    select(User).where(User.id == supervisor_data['seller_id'])
                )

                await self.save(
                    model=Supervisor,
                    supervisor=super_seller,
                    seller=seller,
                    from_date=now().date(),
                    to_date=now().date() + relativedelta(months=supervisor_data['duration']),
                    percentage=supervisor_data['percentage'],
                )

        return seller

    async def update_seller(self, seller_id: int, schema: schemas.SellerUpdateSchema) -> User:
        seller = await self.get_object_or_404(
            select(User).where(
                User.id == seller_id,
                User.role == choices.UserRoles.seller,
            )
        )
        data = schema.model_dump(exclude_unset=True)
        if password := data.pop('password', None):
            data['password'] = hash_password(password)
        return await self.update(obj=seller, **data)

    async def delete_seller(self, seller_id: int) -> dict:
        seller = await self.get_object_or_404(
            select(User).where(
                User.id == seller_id,
                User.role == choices.UserRoles.seller,
            )
        )
        await self.update(obj=seller, is_active=False)
        return {'detail': 'Seller deactivated successfully'}


class SellerDetailService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = _tenant_grpc


    async def get_core_tenants_map(self, seller_id: int) -> dict:
        tenants_id_stmt = await self.db.execute(
            select(Tenant.core_tenant_id).where(Tenant.seller_id == seller_id)
        )
        tenants_id = tenants_id_stmt.scalars().all()
        core_tenants_data = await self._tenant_grpc.get_tenants_by_ids(ids=tenants_id)
        return {t['id']: t for t in core_tenants_data}

    async def seller_detail(self, seller_id: int) -> Any:

        seller = await self.get_object_or_404(
            select(User).where(
                User.id == seller_id,
                User.role == choices.UserRoles.seller,
            )
        )

        tenant_ids = (
            await self.execute(
                select(Tenant.core_tenant_id)
                .where(Tenant.seller_id == seller_id)
            )
        ).scalars().all()

        balance_status = await self._tenant_grpc.get_tenants_balance_status(ids=tenant_ids)

        withdrawn_amount = (await self.execute(
            select(func.coalesce(func.sum(SellerRequest.amount), Decimal('0')))
            .where(
                SellerRequest.seller_id == seller_id,
                SellerRequest.condition == choices.RequestConditions.CONFIRMED,
            )
        )).scalar()

        return {
            'id': seller.id,
            'username': seller.username,
            'full_name': seller.full_name,
            'phone': seller.phone,
            'percentage': seller.percentage,
            'duration': seller.duration,
            'is_active': seller.is_active,
            'trash_data': {
                'must_pay_amount': balance_status['must_paid_amount'],
                'not_paid_amount': balance_status['not_paid_amount'],
                'paid_amount': balance_status['paid_amount'],
                'balance_amount': Decimal('0'),
                'withdrawn_amount': withdrawn_amount,
            },
        }

    async def seller_tenants(self, seller_id: int) -> list[dict]:
        result = await self.db.execute(
            select(
                Tenant.core_tenant_id,
                Tenant.id,
                Tenant.type,
                Tenant.from_date,
                Tenant.to_date,
                Tenant.percentage,
            ).where(Tenant.seller_id == seller_id)
        )

        local_tenants_by_id = {row['core_tenant_id']: dict(row) for row in result.mappings()}

        if not local_tenants_by_id:
            return []

        core_tenants = await self._tenant_grpc.get_tenants_by_ids(
            ids=list(local_tenants_by_id.keys())
        )

        for core_tenant in core_tenants:
            core_tenant['seller_info'] = local_tenants_by_id[core_tenant['id']]

        return core_tenants

    @property
    def _auth_headers(self) -> dict:
        return {'X-Api-Secret-Key': settings.HR_API_SECRET_KEY}

    async def update_monthly_trans(self, pk: int, schema: schemas.MonthlyTransUpdateSchema) -> dict:
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenant-plans/monthly-trans/{pk}/'
        data = schema.model_dump(exclude_none=True, mode='json')
        return await self.httpx_patch(url=url, data=data, headers=self._auth_headers)

    async def seller_assistants(self, seller_id: int) -> Any:
        seller_tenants_count = (
            select(func.count(Tenant.id))
            .where(Tenant.seller_id == Supervisor.seller_id)
            .correlate(Supervisor)
            .scalar_subquery()
        )

        stmt = (
            select(
                Supervisor.id,
                Supervisor.from_date,
                Supervisor.to_date,
                Supervisor.percentage,
                User.full_name,
                seller_tenants_count.label("tenants_count"),
            )
            .join(User, User.id == Supervisor.seller_id)
            .where(Supervisor.supervisor_id == seller_id)
        )

        result = await self.db.execute(stmt)
        return result.mappings().all()



user_service = UserService.annotated('db')
seller_detail_service = SellerDetailService.annotated('db')
