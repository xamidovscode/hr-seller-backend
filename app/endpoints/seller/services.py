from decimal import Decimal

from sqlalchemy import select, func, and_

from app.resources import TenantGrpcClient
from app.resources.services import BaseService
from app.models import Tenant, Supervisor, MonthlyTransaction, User


class SellerService(BaseService):
    user: User

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = TenantGrpcClient()

    async def get_seller_tenants(self):
        payments_sum_exp = func.coalesce(
            func.sum(MonthlyTransaction.amount), Decimal("0.00")
        )

        result = await self.execute(
            select(
                Tenant.id,
                Tenant.core_tenant_id,
                Tenant.type,
                Tenant.from_date,
                Tenant.to_date,
                Tenant.percentage,
                Tenant.seller_id,
                payments_sum_exp.label("payments"),
                (payments_sum_exp * (Tenant.percentage / 100)).label("debit"),
            )
            .outerjoin(
                MonthlyTransaction,
                and_(
                    MonthlyTransaction.tenant_id == Tenant.id,
                    MonthlyTransaction.month >= Tenant.from_date,
                    MonthlyTransaction.month <= Tenant.to_date,
                )

            )
            .where(Tenant.seller_id == self.user.id)
            .group_by(Tenant.id)
        )
        core_tenants_map = await self.get_core_tenants_map(self._tenant_grpc)

        response = []
        for row in result.mappings().all():
            row_dict = dict(row)
            row_dict['core_tenant_data'] = core_tenants_map[row.core_tenant_id]
            response.append(row_dict)

        return response

    async def get_core_tenants_map(self, tenant_grpc) -> dict:
        tenants_id_stmt = await self.db.execute(
            select(Tenant.core_tenant_id).where(Tenant.seller_id == self.user.id)
        )
        tenants_id = tenants_id_stmt.scalars().all()
        core_tenants_data = await tenant_grpc.get_tenants_by_ids(ids=tenants_id)

        return {t['id']: t for t in core_tenants_data}

    async def get_seller_assistants(self):
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
            .where(Supervisor.supervisor_id == self.user.id)
            .subquery()
        )

        final = select(
            stmt,
            (stmt.c.payments_sum * stmt.c.percentage / 100).label("supervisor_share"),
        )
        result = await self.db.execute(final)
        return result.mappings().all()


seller_service = SellerService.annotated('db', 'user')