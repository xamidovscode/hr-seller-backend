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

        calc = SellerBalanceCalculator(self.db)
        balance_info = await calc.bulk_breakdown([seller_id])

        return {
            'id': seller.id,
            'username': seller.username,
            'full_name': seller.full_name,
            'phone': seller.phone,
            'percentage': seller.percentage,
            'duration': seller.duration,
            'is_active': seller.is_active,
            'balance_info': balance_info[seller_id],
            'trash_data': {
                'must_pay_amount': Decimal('76653354'),
                'not_paid_amount': Decimal('38705914'),
                'paid_amount': Decimal('37947440'),
                'balance_amount': Decimal('0'),
                'withdrawn_amount': Decimal('-7300000'),
            }
        }

    async def seller_requests(self, seller_id: int) -> Any:
        return [
            {
                'id': 1,
                'date': '2026-01-01',
                'amount': Decimal('76543210.50'),
                'balance': Decimal('152340000.75'),
            },
            {
                'id': 2,
                'date': '2026-02-01',
                'amount': Decimal('81245000.00'),
                'balance': Decimal('71115000.75'),
            },
            {
                'id': 3,
                'date': '2026-03-01',
                'amount': Decimal('68990540.25'),
                'balance': Decimal('21450000.50'),
            },
            {
                'id': 4,
                'date': '2026-04-01',
                'amount': Decimal('21450000.50'),
                'balance': Decimal('0.00'),
            },
        ]

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

        fake_plans_data = [
            {
                'id': 92,
                'name': "IMB TECH Mchj",
                'active_plan_amount': Decimal('1500000'),
                'employee_count': 88,
            }
        ]

        plans_history = [
                {
                    'id': 92,
                    "month": '2026-01-01',
                    'amount': Decimal('1500000'),
                    'status': 'paid',
                },
                {
                    'id': 93,
                    "month": '2026-02-01',
                    'amount': Decimal('3500000'),
                    'status': '',
                },
                {
                    'id': 94,
                    "month": '2026-03-01',
                    'amount': Decimal('2500000'),
                    'status': 'invoice',
                },
                {
                    'id': 95,
                    "month": '2026-04-01',
                    'amount': Decimal('1500000'),
                    'status': 'w',
                },
        ]

        response = []
        for row in result.mappings().all():
            row_dict = dict(row)
            row_dict['core_tenant_data'] = fake_plans_data
            row_dict['plans_history'] = plans_history
            response.append(row_dict)

        return response

    # async def seller_tenants(self, seller_id: int) -> Any:
    #     payments_sum_expr = func.coalesce(
    #         func.sum(MonthlyTransaction.amount), Decimal("0.00")
    #     )
    #
    #     stmt = (
    #         select(
    #             Tenant.id,
    #             Tenant.core_tenant_id,
    #             Tenant.type,
    #             Tenant.from_date,
    #             Tenant.to_date,
    #             Tenant.percentage,
    #             payments_sum_expr.label("payments_sum"),
    #             (payments_sum_expr * (Tenant.percentage / 100)).label("seller_debit"),
    #         )
    #         .outerjoin(
    #             MonthlyTransaction,
    #             and_(
    #                 MonthlyTransaction.tenant_id == Tenant.id,
    #                 MonthlyTransaction.month >= Tenant.from_date,
    #                 MonthlyTransaction.month <= Tenant.to_date,
    #             ),
    #         )
    #         .where(Tenant.seller_id == seller_id)
    #         .group_by(
    #             Tenant.id,
    #             Tenant.core_tenant_id,
    #             Tenant.type,
    #             Tenant.from_date,
    #             Tenant.to_date,
    #             Tenant.percentage,
    #         )
    #     )
    #     result = await self.db.execute(stmt)
    #     core_tenants_map = await self.get_core_tenants_map(seller_id)
    #
    #     response = []
    #     for row in result.mappings().all():
    #         row_dict = dict(row)
    #         row_dict['core_tenant_data'] = core_tenants_map.get(row.core_tenant_id, {})
    #         response.append(row_dict)
    #
    #     return response

    async def seller_assistants(self, seller_id: int) -> Any:
        seller_tenants_count = (
            select(func.count(Tenant.id))
            .where(Tenant.seller_id == Supervisor.seller_id)
            .correlate(Supervisor)
            .scalar_subquery()
        )

        payments_sum = (
            select(func.coalesce(func.sum(MonthlyTransaction.amount), 0))
            .join(Tenant, Tenant.id == MonthlyTransaction.tenant_id)
            .where(
                Tenant.seller_id == Supervisor.seller_id,
                MonthlyTransaction.month >= Supervisor.from_date,
                MonthlyTransaction.month <= Supervisor.to_date,
            )
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
                payments_sum.label("payments_sum"),
            )
            .join(User, User.id == Supervisor.seller_id)
            .where(Supervisor.supervisor_id == seller_id)
            .subquery()
        )

        final = select(
            stmt,
            (stmt.c.payments_sum * stmt.c.percentage / 100).label("supervisor_share"),
        )
        result = await self.db.execute(final)
        return result.mappings().all()



user_service = UserService.annotated('db')
seller_detail_service = SellerDetailService.annotated('db')
