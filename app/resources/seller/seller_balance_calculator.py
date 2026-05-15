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

    def __init__(self, db: AsyncSession):
        self.db = db

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
            for row in await self.db.execute(earned_seller_stmt)
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
            for row in await self.db.execute(earned_super_stmt)
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
            for row in await self.db.execute(withdrawn_stmt)
        }

        # 4. Tenants count
        tenants_cnt_stmt = (
            select(Tenant.seller_id.label('sid'), func.count(Tenant.id).label('cnt'))
            .where(Tenant.seller_id.in_(seller_ids))
            .group_by(Tenant.seller_id)
        )
        tenants_cnt = {
            row.sid: row.cnt
            for row in await self.db.execute(tenants_cnt_stmt)
        }

        # 5. O'zi supervisor bo'lganlari (ixtiyoriy, kerak bo'lsa)
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
            for row in await self.db.execute(supervised_cnt_stmt)
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
                'supervised_count': supervised_cnt.get(sid, 0),
            }
        return result