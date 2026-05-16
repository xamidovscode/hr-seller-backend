from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    Supervisor,
    SellerRequest,
    Tenant,
    MonthlyTransaction, User
)
from app.resources.seller.seller_balance_calculator import SellerBalanceCalculator


class SelleDetail:
    """
    Seller ning balansi detail ko'rinishda hamma datalar bilan birgalikda

    -------- Faqat bitta seller uchun --------
    """

    def __init__(self, db: AsyncSession, seller_id: int):
        self.db = db
        self.seller_id = seller_id

    async def tenants_data(self, tenant_grpc):
        stmt = (
            select(
                Tenant.id,
                Tenant.core_tenant_id,
                Tenant.type,
                Tenant.from_date,
                Tenant.to_date,
                Tenant.percentage,
            )
            .where(Tenant.seller_id == self.seller_id)
        )
        result = await self.db.execute(stmt)
        core_tenants_map = await self.get_core_tenants_map(tenant_grpc)

        response = []
        for row in result.mappings().all():
            row_dict = dict(row)
            row_dict['core_tenant_data'] = core_tenants_map[row.core_tenant_id]
            response.append(row_dict)

        return response

    async def get_core_tenants_map(self, tenant_grpc) -> dict:
        tenants_id_stmt = await self.db.execute(
            select(Tenant.core_tenant_id).where(Tenant.seller_id == self.seller_id)
        )
        tenants_id = tenants_id_stmt.scalars().all()
        core_tenants_data = await tenant_grpc.get_tenants_by_ids(ids=tenants_id)

        return {t['id']: t for t in core_tenants_data}

    async def assistants_data(self):
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
            .where(Supervisor.supervisor_id == self.seller_id)
            .subquery()
        )

        final = select(
            stmt,
            (stmt.c.payments_sum * stmt.c.percentage / 100).label("supervisor_share"),
        )
        result = await self.db.execute(final)
        return result.mappings().all()

    async def seller_requests(self):
        stmt = (
            select(
                SellerRequest.id,
                SellerRequest.amount,
                SellerRequest.date,
                SellerRequest.condition,
            )
            .where(SellerRequest.seller_id == self.seller_id)
        )
        result = await self.db.execute(stmt)
        return result.mappings().all()

    async def detail_balance(self):
        calc = SellerBalanceCalculator(self.db)
        balance_info = await calc.bulk_breakdown([self.seller_id])
        return balance_info[self.seller_id]


