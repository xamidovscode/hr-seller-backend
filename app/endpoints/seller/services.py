from decimal import Decimal

from decimal import Decimal

from sqlalchemy import select, func

from app.resources import TenantGrpcClient
from app.resources.services import BaseService
from app.models import Tenant, Supervisor, User


_tenant_grpc = TenantGrpcClient()


class SellerService(BaseService):
    user: User

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = _tenant_grpc

    async def get_seller_tenants(self):
        result = await self.execute(
            select(
                Tenant.id,
                Tenant.core_tenant_id,
                Tenant.type,
                Tenant.from_date,
                Tenant.to_date,
                Tenant.percentage,
                Tenant.seller_id,
            )
            .where(Tenant.seller_id == self.user.id)
        )
        core_tenants_map = await self.get_core_tenants_map(self._tenant_grpc)

        response = []
        for row in result.mappings().all():
            row_dict = dict(row)
            row_dict['payments'] = Decimal('0')
            row_dict['debit'] = Decimal('0')
            row_dict['core_tenant_data'] = core_tenants_map.get(row.core_tenant_id, {})
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
            .where(Supervisor.supervisor_id == self.user.id)
            .subquery()
        )

        final = select(
            stmt,
            (Decimal('0') * stmt.c.percentage / 100).label("supervisor_share"),
        )
        result = await self.db.execute(final)
        return result.mappings().all()


seller_service = SellerService.annotated('db', 'user')