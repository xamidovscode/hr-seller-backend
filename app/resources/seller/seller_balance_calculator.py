__all__ = (
    'SellerBalanceCalculator',
)

from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Tenant,
    Supervisor,
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

        # 3. Withdrawn
        withdrawn_stmt = (
            select(
                SellerRequest.seller_id.label('sid'),
                func.coalesce(func.sum(SellerRequest.amount), Decimal('0')).label('amount'),
            )
            .where(
                SellerRequest.seller_id.in_(seller_ids),
                SellerRequest.condition == RequestConditions.CONFIRMED,
            )
            .group_by(SellerRequest.seller_id)
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

        # 5. O'zi supervisor bo'lganlari
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

        # as_seller va as_supervisor core service gRPC dan keladi
        result = {}
        for sid in seller_ids:
            w = withdrawn.get(sid, Decimal('0'))
            result[sid] = {
                'as_seller': Decimal('0'),
                'as_supervisor': Decimal('0'),
                'withdrawn': w,
                'balance': Decimal('0') - w,
                'tenants_count': tenants_cnt.get(sid, 0),
                'supervised_count': supervised_cnt.get(sid, 0),
            }
        return result