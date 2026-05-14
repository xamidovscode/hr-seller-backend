import asyncio

from app.endpoints.tenants.schemas import TenantCreateSchema
from app.resources.services import BaseService
from app.resources.grpc.tenant import get_tenants
from app.core.settings import settings


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

    async def create_tenant(self, schema: TenantCreateSchema):
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenants/'
        data = schema.model_dump()
        seller_id = data.pop('seller_id')

        response = await self.httpx_post(url=url, data=data)

        tenant_id = response['id']
        return response


tenant_service = TenantService.annotated('db')