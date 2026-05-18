from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.settings import settings
from app.endpoints.tenants.schemas import (
    TenantCreateSchema, TenantUpdateSchema,
    MonthlyTransactionCreateSchema, MonthlyTransactionUpdateSchema,
)
from app.models import tenants, users
from app.models.choices import TenantTypes
from app.resources.services import BaseService, TenantGrpcClient, PlansGrpcClient
from app.utils.time import now


_tenant_grpc = TenantGrpcClient()
_plans_grpc = PlansGrpcClient()


class TenantService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = _tenant_grpc
        self._plans_grpc = _plans_grpc

    async def get_all_tenants(self):
        local_tenants = await self.get_all(select(tenants.Tenant))
        core_tenants = await self._tenant_grpc.get_tenants()

        local_tenant_data = {tenant.core_tenant_id: tenant for tenant in local_tenants}

        return [
            {
                **tenant,
                'tenant_type': "imb_hr",
                "seller_info": local_tenant_data.get(tenant['id'], {}),
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
                    core_tenant_id=0,
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
                    core_tenant_id=response['id'],
                )
        return response

    async def tenant_detail(self, core_tenant_id: int):
        local_tenant = await self.get_object_or_404(
            select(tenants.Tenant)
            .options(selectinload(tenants.Tenant.seller))
            .where(tenants.Tenant.core_tenant_id == core_tenant_id)
        )

        core_tenant_data = await self._tenant_grpc.get_tenant_by_id(pk=core_tenant_id)
        active_plans_data = await self._plans_grpc.get_tenant_active_plan(tenant_id=core_tenant_id)

        from_date = local_tenant.from_date
        to_date = local_tenant.to_date
        percentage = local_tenant.percentage

        monthly_transactions = await self.get_all(
            select(tenants.MonthlyTransaction).where(tenants.MonthlyTransaction.tenant_id == local_tenant.id)
        )

        for mt in monthly_transactions:

            if from_date <= mt.month <= to_date:
                mt.seller_amount = mt.amount * (percentage / 100)
            else:
                mt.seller_amount = 0

        core_tenant_data.update({
            'seller_id': local_tenant.seller_id,
            'seller_name': local_tenant.seller.full_name,
            'from_date': from_date,
            'to_date': to_date,
            'percentage': percentage,
            'monthly_transactions': monthly_transactions,
            'active_plans': active_plans_data,
        })

        return core_tenant_data

    async def tenant_update(self, tenant_id: int, schema: TenantUpdateSchema):
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenants/{tenant_id}/'
        data = schema.model_dump()
        response = await self.httpx_patch(url=url, data=data)
        return response

tenant_service = TenantService.annotated('db')


class MonthlyTransactionService(BaseService):

    async def create_transaction(self, schema: MonthlyTransactionCreateSchema) -> tenants.MonthlyTransaction:
        await self.get_object_or_404(
            select(tenants.Tenant).where(tenants.Tenant.core_tenant_id == schema.tenant_id)
        )
        return await self.save(model=tenants.MonthlyTransaction, schema=schema)

    async def update_transaction(self, pk: int, schema: MonthlyTransactionUpdateSchema) -> tenants.MonthlyTransaction:
        obj = await self.get_object_or_404(
            select(tenants.MonthlyTransaction).where(tenants.MonthlyTransaction.id == pk)
        )
        return await self.update(obj=obj, schema=schema)

    async def delete_transaction(self, pk: int) -> dict:
        obj = await self.get_object_or_404(
            select(tenants.MonthlyTransaction).where(tenants.MonthlyTransaction.id == pk)
        )
        return await self.remove(obj)


monthly_trans_service = MonthlyTransactionService.annotated('db')


