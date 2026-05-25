__all__ = (
    'SellerBalanceCalculator',
)

import asyncio
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Tenant,
    Supervisor,
    SellerRequest,
)
from app.models.choices import RequestConditions
from app.resources.services.grpc.tenant_plans import TenantPlansGrpcClient


class SellerBalanceCalculator:
    """Seller balansini real-time hisoblovchi service.

    Balans = (o'z tenantlardan ulush)
           + (supervisor sifatida ulush)
           − (CONFIRMED yechib olishlar)
    """

    def __init__(self, db: AsyncSession, tenant_plans_grpc: TenantPlansGrpcClient):
        self.db = db
        self._tenant_plans_grpc = tenant_plans_grpc

    async def calculate_as_seller(self, seller_id: int) -> Decimal:
        """Seller ning o'z tenantlaridan olgan ulushini hisoblaydi.

        Har bir tenant uchun core servisga (tenant_id, from_date, to_date)
        yuboriladi, core SUM(paid_amount) qaytaradi.
        Seller backendda: sum * percentage / 100.
        """
        stmt = select(
            Tenant.core_tenant_id,
            Tenant.from_date,
            Tenant.to_date,
            Tenant.percentage,
        ).where(Tenant.seller_id == seller_id)

        rows = (await self.db.execute(stmt)).mappings().all()
        if not rows:
            return Decimal('0')

        total = Decimal('0')
        for row in rows:
            paid_sum = await self._tenant_plans_grpc.get_tenant_paid_amount_sum(
                tenant_id=row.core_tenant_id,
                from_date=str(row.from_date),
                to_date=str(row.to_date),
            )
            total += Decimal(str(paid_sum)) * row.percentage / 100

        return total

    async def calculate_as_supervisor(self, seller_id: int) -> Decimal:
        """Seller supervisor sifatida olgan ulushini hisoblaydi.

        Seller qaysi sellerlarga supervisor bo'lsa, ularning tenantlaridan
        Supervisor.from_date..to_date oralig'idagi paid_amount_sum * percentage / 100.
        """
        # seller supervise qilgan barcha yozuvlar + ularning seller_id lari
        sup_rows = (
            await self.db.execute(
                select(
                    Supervisor.seller_id,
                    Supervisor.from_date,
                    Supervisor.to_date,
                    Supervisor.percentage,
                ).where(Supervisor.supervisor_id == seller_id)
            )
        ).mappings().all()

        if not sup_rows:
            return Decimal('0')

        supervised_seller_ids = [r.seller_id for r in sup_rows]

        # har bir supervised seller ning core_tenant_id lari
        tenant_rows = (
            await self.db.execute(
                select(Tenant.seller_id, Tenant.core_tenant_id)
                .where(Tenant.seller_id.in_(supervised_seller_ids))
            )
        ).mappings().all()

        # seller_id -> [core_tenant_id, ...]
        tenants_by_seller: dict[int, list[int]] = {}
        for t in tenant_rows:
            tenants_by_seller.setdefault(t.seller_id, []).append(t.core_tenant_id)

        total = Decimal('0')
        for sup in sup_rows:
            core_ids = tenants_by_seller.get(sup.seller_id, [])
            for core_tenant_id in core_ids:
                paid_sum = await self._tenant_plans_grpc.get_tenant_paid_amount_sum(
                    tenant_id=core_tenant_id,
                    from_date=str(sup.from_date),
                    to_date=str(sup.to_date),
                )
                total += Decimal(str(paid_sum)) * sup.percentage / 100

        return total

    async def get_balance(self, seller_id: int) -> dict:
        """Seller ning umumiy balans hisobini qaytaradi."""
        as_seller, as_supervisor, withdrawn = await asyncio.gather(
            self.calculate_as_seller(seller_id),
            self.calculate_as_supervisor(seller_id),
            self._get_withdrawn(seller_id),
        )
        total_income = as_seller + as_supervisor
        return {
            'as_seller': as_seller,
            'as_supervisor': as_supervisor,
            'total_income': total_income,
            'withdrawn': withdrawn,
            'balance': total_income - withdrawn,
        }

    async def _get_withdrawn(self, seller_id: int) -> Decimal:
        result = await self.db.execute(
            select(
                func.coalesce(func.sum(SellerRequest.amount), Decimal('0'))
            ).where(
                SellerRequest.seller_id == seller_id,
                SellerRequest.condition == RequestConditions.CONFIRMED,
            )
        )
        return result.scalar()