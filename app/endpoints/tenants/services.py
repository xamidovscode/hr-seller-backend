import asyncio

from app.resources.services import BaseService
from app.resources.grpc.tenant import get_tenants



class TenantService(BaseService):

    async def get_all_tenants(self):
        tenants = await asyncio.to_thread(get_tenants)
        result = []

        for tenant in tenants:
            result.append({
                "id": tenant.id,
                "name": tenant.name,
                "schema_name": tenant.schema_name,
                "created_on": tenant.created_on,
                "activated_at": tenant.activated_at,
                "deadline": tenant.deadline,
                "is_active": tenant.is_active,
                "on_trial": tenant.on_trial,
                "is_deleted": tenant.is_deleted,
            })

        return result


tenant_service = TenantService.annotated('db')