from dateutil.relativedelta import relativedelta
from sqlalchemy import select

from app.core.settings import settings
from app.endpoints.tenants.schemas import TenantCreateSchema
from app.models import tenants, users
from app.models.choices import TenantTypes
from app.resources.services import BaseService, TenantGrpcService
from app.utils.time import now


class TenantService(BaseService, TenantGrpcService):

    async def get_all_tenants(self):
        local_tenants = await self.get_all(select(tenants.Tenant))
        core_tenants = await self.get_grpc_tenants()

        local_tenant_data = {tenant.tenant_id: tenant for tenant in local_tenants}

        return [
            {
                "id": tenant.id,
                "name": tenant.name,
                "schema_name": tenant.schema_name,
                "created_on": tenant.created_on,
                "activated_at": tenant.activated_at,
                "deadline": tenant.deadline,
                "is_active": tenant.is_active,
                "on_trial": tenant.on_trial,
                "is_deleted": tenant.is_deleted,
                "seller_info": local_tenant_data.get(tenant.id, {}),
            }
            for tenant in core_tenants
        ]

    async def create_tenant(self, schema: TenantCreateSchema):
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenants/'
        data = schema.model_dump()
        seller_id = data.pop('seller_id', None)
        tenant = None

        async with self.atomic():

            if seller_id:
                    seller = await self.get_object_or_404(
                        select(users.User).where(users.User.id == seller_id)
                    )

                    tenant = await self.save(
                        model=tenants.Tenant,
                        tenant_id=0,
                        type=TenantTypes.IMB_HR,
                        from_date=now().date(),
                        to_date=now().date() + relativedelta(months=seller.duration),
                        percentage=seller.percentage,
                        seller=seller,
                    )

            response = await self.httpx_post(url=url, data=data)

            if tenant:
                await self.update(
                    obj=tenant,
                    tenant_id=response['id'],
                )
        return response


tenant_service = TenantService.annotated('db')