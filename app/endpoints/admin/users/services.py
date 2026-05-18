from decimal import Decimal
from typing import List, Any

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, func, and_

from app.models import (
    choices,
    SellerRequest,
    User,
    Supervisor,
    MonthlyTransaction,
    Tenant,
)
from app.resources import BaseService, TenantGrpcClient
from app.resources.seller.seller_balance_calculator import SellerBalanceCalculator
from app.resources.seller.seller_balance_detail import SellerDetail
from app.utils import hash_password
from app.utils.time import now
from . import schemas

_tenant_grpc = TenantGrpcClient()


class UserService(BaseService):

    async def sellers_list(self) -> List[dict[str, Any]]:
        sellers = await self.get_all(
            select(User).where(User.role == choices.UserRoles.seller)
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
        return await self.update(obj=seller, schema=schema)

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

        sbd = SellerDetail(db=self.db, seller_id=seller_id)

        return {
            'id': seller.id,
            'username': seller.username,
            'full_name': seller.full_name,
            'phone': seller.phone,
            'percentage': seller.percentage,
            'duration': seller.duration,
            'is_active': seller.is_active,
            'assistants': await sbd.assistants_data(),
            'tenants': await sbd.tenants_data(tenant_grpc=self._tenant_grpc),
            # 'requests': await sbd.seller_requests(),
            'balance_info': await sbd.detail_balance(),
        }

    async def seller_requests(self, seller_id: int) -> Any:
        stmt = (
            select(
                SellerRequest.id,
                SellerRequest.amount,
                SellerRequest.date,
                SellerRequest.condition,
            )
            .where(SellerRequest.seller_id == seller_id)
        )
        result = await self.db.execute(stmt)
        return result.mappings().all()

    async def seller_tenants(self, seller_id: int) -> Any:
        payments_sum_expr = func.coalesce(
            func.sum(MonthlyTransaction.amount), Decimal("0.00")
        )

        stmt = (
            select(
                Tenant.id,
                Tenant.core_tenant_id,
                Tenant.type,
                Tenant.from_date,
                Tenant.to_date,
                Tenant.percentage,
                payments_sum_expr.label("payments_sum"),
                (payments_sum_expr * (Tenant.percentage / 100)).label("seller_debit"),
            )
            .outerjoin(
                MonthlyTransaction,
                and_(
                    MonthlyTransaction.tenant_id == Tenant.id,
                    MonthlyTransaction.month >= Tenant.from_date,
                    MonthlyTransaction.month <= Tenant.to_date,
                ),
            )
            .where(Tenant.seller_id == seller_id)
            .group_by(
                Tenant.id,
                Tenant.core_tenant_id,
                Tenant.type,
                Tenant.from_date,
                Tenant.to_date,
                Tenant.percentage,
            )
        )
        result = await self.db.execute(stmt)
        core_tenants_map = await self.get_core_tenants_map(seller_id)

        response = []
        for row in result.mappings().all():
            row_dict = dict(row)
            row_dict['core_tenant_data'] = core_tenants_map.get(row.core_tenant_id, {})
            response.append(row_dict)

        return response


user_service = UserService.annotated('db')
seller_detail_service = SellerDetailService.annotated('db')
