__all__ = (
    'SellerBalanceCalculator',
)

from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Tenant,
    Supervisor,
    MonthlyTransaction,
    SellerTransactions,
    SellerRequest,
)
from app.models.choices import RequestConditions


class SellerBalanceCalculator:
    """Seller balansini real-time hisoblovchi service.

    Balans = (o'z tenantlardan ulush)
           + (supervisor sifatida ulush)
           − (CONFIRMED yechib olishlar)
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def earned_as_seller(self, seller_id: int) -> Decimal:
        stmt = (
            select(
                func.coalesce(
                    func.sum(
                        MonthlyTransaction.amount * Tenant.percentage / Decimal('100')
                    ),
                    Decimal('0'),
                )
            )
            .select_from(MonthlyTransaction)
            .join(Tenant, Tenant.id == MonthlyTransaction.tenant_id)
            .where(
                Tenant.seller_id == seller_id,
                MonthlyTransaction.month >= Tenant.from_date,
                MonthlyTransaction.month <= Tenant.to_date,
            )
        )
        return (await self.session.scalar(stmt)) or Decimal('0.00')

    async def earned_as_supervisor(self, seller_id: int) -> Decimal:
        stmt = (
            select(
                func.coalesce(
                    func.sum(
                        MonthlyTransaction.amount * Supervisor.percentage / Decimal('100')
                    ),
                    Decimal('0'),
                )
            )
            .select_from(MonthlyTransaction)
            .join(Tenant, Tenant.id == MonthlyTransaction.tenant_id)
            .join(Supervisor, Supervisor.seller_id == Tenant.seller_id)
            .where(
                Supervisor.supervisor_id == seller_id,
                MonthlyTransaction.month >= Tenant.from_date,
                MonthlyTransaction.month <= Tenant.to_date,
                MonthlyTransaction.month >= Supervisor.from_date,
                MonthlyTransaction.month <= Supervisor.to_date,
            )
        )
        return (await self.session.scalar(stmt)) or Decimal('0.00')

    async def withdrawn(self, seller_id: int) -> Decimal:
        stmt = (
            select(func.coalesce(func.sum(SellerRequest.amount), Decimal('0')))
            .join(
                SellerTransactions,
                SellerTransactions.id == SellerRequest.seller_transaction_id,
            )
            .where(
                SellerTransactions.seller_id == seller_id,
                SellerRequest.condition == RequestConditions.CONFIRMED,
            )
        )
        return (await self.session.scalar(stmt)) or Decimal('0.00')

    async def balance(self, seller_id: int) -> Decimal:
        as_seller = await self.earned_as_seller(seller_id)
        as_supervisor = await self.earned_as_supervisor(seller_id)
        withdrawn = await self.withdrawn(seller_id)
        return as_seller + as_supervisor - withdrawn

    async def tenants_count(self, seller_id: int) -> int:
        """Seller olib kelgan tenantlar soni."""
        stmt = (
            select(func.count(Tenant.id))
            .where(Tenant.seller_id == seller_id)
        )
        return await self.session.scalar(stmt) or 0

    async def supervised_count(self, seller_id: int) -> int:
        """Seller supervisor bo'lgan boshqa sellerlar soni."""
        stmt = (
            select(func.count(Supervisor.id))
            .where(Supervisor.supervisor_id == seller_id)
        )
        return await self.session.scalar(stmt) or 0

    async def breakdown(self, seller_id: int) -> dict:
        as_seller = await self.earned_as_seller(seller_id)
        as_supervisor = await self.earned_as_supervisor(seller_id)
        withdrawn = await self.withdrawn(seller_id)
        return {
            # Pul
            'as_seller': as_seller,
            'as_supervisor': as_supervisor,
            'withdrawn': withdrawn,
            'balance': as_seller + as_supervisor - withdrawn,
            # Statistika
            'tenants_count': await self.tenants_count(seller_id),
            'supervised_count': await self.supervised_count(seller_id),
        }

    async def bulk_breakdown(
            self, seller_ids: list[int],
    ) -> dict[int, dict]:
        """Bir nechta seller uchun bir martada statistika.

        Natija: {seller_id: {balance, as_seller, ..., tenants_count, ...}}
        """
        if not seller_ids:
            return {}

        # 1. O'z tenantlaridan ulush (har biri uchun)
        earned_seller_stmt = (
            select(
                Tenant.seller_id.label('sid'),
                func.coalesce(
                    func.sum(
                        MonthlyTransaction.amount * Tenant.percentage / Decimal('100')
                    ),
                    Decimal('0'),
                ).label('amount'),
            )
            .select_from(MonthlyTransaction)
            .join(Tenant, Tenant.id == MonthlyTransaction.tenant_id)
            .where(
                Tenant.seller_id.in_(seller_ids),
                MonthlyTransaction.month >= Tenant.from_date,
                MonthlyTransaction.month <= Tenant.to_date,
            )
            .group_by(Tenant.seller_id)
        )
        earned_seller = {
            row.sid: row.amount
            for row in await self.session.execute(earned_seller_stmt)
        }

        # 2. Supervisor sifatida
        earned_super_stmt = (
            select(
                Supervisor.supervisor_id.label('sid'),
                func.coalesce(
                    func.sum(
                        MonthlyTransaction.amount * Supervisor.percentage / Decimal('100')
                    ),
                    Decimal('0'),
                ).label('amount'),
            )
            .select_from(MonthlyTransaction)
            .join(Tenant, Tenant.id == MonthlyTransaction.tenant_id)
            .join(Supervisor, Supervisor.seller_id == Tenant.seller_id)
            .where(
                Supervisor.supervisor_id.in_(seller_ids),
                MonthlyTransaction.month >= Tenant.from_date,
                MonthlyTransaction.month <= Tenant.to_date,
                MonthlyTransaction.month >= Supervisor.from_date,
                MonthlyTransaction.month <= Supervisor.to_date,
            )
            .group_by(Supervisor.supervisor_id)
        )
        earned_super = {
            row.sid: row.amount
            for row in await self.session.execute(earned_super_stmt)
        }

        # 3. Withdrawn
        withdrawn_stmt = (
            select(
                SellerTransactions.seller_id.label('sid'),
                func.coalesce(func.sum(SellerRequest.amount), Decimal('0')).label('amount'),
            )
            .join(
                SellerTransactions,
                SellerTransactions.id == SellerRequest.seller_transaction_id,
            )
            .where(
                SellerTransactions.seller_id.in_(seller_ids),
                SellerRequest.condition == RequestConditions.CONFIRMED,
            )
            .group_by(SellerTransactions.seller_id)
        )
        withdrawn = {
            row.sid: row.amount
            for row in await self.session.execute(withdrawn_stmt)
        }

        # 4. Tenants count
        tenants_cnt_stmt = (
            select(Tenant.seller_id.label('sid'), func.count(Tenant.id).label('cnt'))
            .where(Tenant.seller_id.in_(seller_ids))
            .group_by(Tenant.seller_id)
        )
        tenants_cnt = {
            row.sid: row.cnt
            for row in await self.session.execute(tenants_cnt_stmt)
        }

        # 5. Supervisorlar soni (unga supervisor bo'lganlar)
        supervisors_cnt_stmt = (
            select(Supervisor.seller_id.label('sid'), func.count(Supervisor.id).label('cnt'))
            .where(Supervisor.seller_id.in_(seller_ids))
            .group_by(Supervisor.seller_id)
        )
        supervisors_cnt = {
            row.sid: row.cnt
            for row in await self.session.execute(supervisors_cnt_stmt)
        }

        # 6. O'zi supervisor bo'lganlari (ixtiyoriy, kerak bo'lsa)
        supervised_cnt_stmt = (
            select(
                Supervisor.supervisor_id.label('sid'),
                func.count(Supervisor.id).label('cnt'),
            )
            .where(Supervisor.supervisor_id.in_(seller_ids))
            .group_by(Supervisor.supervisor_id)
        )
        supervised_cnt = {
            row.sid: row.cnt
            for row in await self.session.execute(supervised_cnt_stmt)
        }

        # Yig'amiz
        result = {}
        for sid in seller_ids:
            a = earned_seller.get(sid, Decimal('0'))
            s = earned_super.get(sid, Decimal('0'))
            w = withdrawn.get(sid, Decimal('0'))
            result[sid] = {
                'as_seller': a,
                'as_supervisor': s,
                'withdrawn': w,
                'balance': a + s - w,
                'tenants_count': tenants_cnt.get(sid, 0),
                'supervisors_count': supervisors_cnt.get(sid, 0),
                'supervised_count': supervised_cnt.get(sid, 0),
            }
        return result