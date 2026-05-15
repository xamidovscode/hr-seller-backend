from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Supervisor,
    SellerRequest,
    Tenant,
    MonthlyTransaction
)


class SellerBalanceDetail:
    """
    Seller ning balansi detail ko'rinishda hamma datalar bilan birgalikda

    -------- Faqat bitta seller uchun --------
    """

    def __init__(self, db: AsyncSession, seller_id: int):
        self.db = db
        self.seller_id = seller_id

    async def tenants_data(self):
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
        return result.mappings().all()

    async def assistants_data(self):
        stmt = (
            select(
                Supervisor.id,
                Supervisor.from_date,
                Supervisor.to_date,
                Supervisor.percentage,
            )
            .where(Supervisor.supervisor_id == self.seller_id)
        )
        result = await self.db.execute(stmt)
        return result.mappings().all()

    async def seller_requests(self):
        stmt = (
            select(
                SellerRequest.id,
                SellerRequest.amount,
                SellerRequest.date,
                SellerRequest.condition,
            )
        )
        result = await self.db.execute(stmt)
        return result.mappings().all()

    async def detail_balance(self):
        pass

