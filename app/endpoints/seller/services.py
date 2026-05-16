from sqlalchemy import select

from app.resources.services import BaseService
from app.models import tenants, users



class SellerService(BaseService):
    user: users.User

    async def get_seller_tenants(self):
        result = await self.execute(
            select(
                tenants.Tenant.id,
                tenants.Tenant.core_tenant_id,
                tenants.Tenant.type,
                tenants.Tenant.from_date,
                tenants.Tenant.to_date,
                tenants.Tenant.percentage,
                tenants.Tenant.seller_id,
            )
            .where(tenants.Tenant.seller_id == self.user.id)
        )

        return result.mappings().all()


seller_service = SellerService.annotated('db', 'user')