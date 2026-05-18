from decimal import Decimal

from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.settings import settings
from app.models import tenants, users
from app.models.choices import TenantTypes
from app.resources.services import BaseService, TenantGrpcClient, PlansGrpcClient
from app.utils.time import now
from . import schemas


_tenant_grpc = TenantGrpcClient()
_plans_grpc = PlansGrpcClient()


class TenantService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = _tenant_grpc

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

    async def create_tenant(self, schema: schemas.TenantCreateSchema):
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenants/'
        data = schema.model_dump()
        seller_id = data.pop('seller_id', None)

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
            else:
                tenant = await self.save(
                    model=tenants.Tenant,
                    core_tenant_id=0,
                    type=TenantTypes.IMB_HR,
                    from_date=now().date(),
                    to_date=now().date(),
                    percentage=Decimal("0.00"),
                )

            response = await self.httpx_post(url=url, data=data)
            await self.update(obj=tenant, core_tenant_id=response['id'])

        return response

    async def tenant_update(self, core_tenant_id: int, schema: schemas.TenantUpdateSchema):
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenants/{core_tenant_id}/'
        data = schema.model_dump()
        response = await self.httpx_patch(url=url, data=data)
        return response


class TenantDetailService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = _tenant_grpc
        self._plans_grpc = _plans_grpc

    async def tenant_detail(self, core_tenant_id: int):
        core_tenant_data = await self._tenant_grpc.get_tenant_by_id(pk=core_tenant_id)
        return core_tenant_data

    async def get_active_plans(self, core_tenant_id: int):
        active_plans_data = await self._plans_grpc.get_tenant_active_plan(tenant_id=core_tenant_id)
        return active_plans_data

    async def get_monthly_transactions(self, core_tenant_id: int):
        local_tenant = await self.get_object_or_404(
            select(tenants.Tenant).where(tenants.Tenant.core_tenant_id == core_tenant_id)
        )
        stmt = (
            select(
                tenants.MonthlyTransaction.id,
                tenants.MonthlyTransaction.created_at,
                tenants.MonthlyTransaction.service_id,
                tenants.MonthlyTransaction.month,
                tenants.MonthlyTransaction.amount,
            )
            .where(tenants.MonthlyTransaction.tenant_id == local_tenant.id)
        )
        result = await self.execute(stmt)
        return result.mappings().all()


class MonthlyTransactionService(BaseService):

    async def create_transaction(self, schema: schemas.MonthlyTransactionCreateSchema) -> tenants.MonthlyTransaction:
        local_tenant = await self.get_object_or_404(
            select(tenants.Tenant).where(tenants.Tenant.core_tenant_id == schema.tenant_id)
        )
        data = {
            'month': schema.month,
            'amount': schema.amount,
            'tenant_id': local_tenant.id,
            'service_id': 0,
        }
        return await self.save(model=tenants.MonthlyTransaction, **data)

    async def update_transaction(self, pk: int, schema: schemas.MonthlyTransactionUpdateSchema) -> tenants.MonthlyTransaction:
        obj = await self.get_object_or_404(
            select(tenants.MonthlyTransaction).where(tenants.MonthlyTransaction.id == pk)
        )
        return await self.update(obj=obj, schema=schema)

    async def delete_transaction(self, pk: int) -> dict:
        obj = await self.get_object_or_404(
            select(tenants.MonthlyTransaction).where(tenants.MonthlyTransaction.id == pk)
        )
        return await self.remove(obj)


class TelegramChatService(BaseService):

    async def get_all_chats(self):
        stmt = select(tenants.TelegramChat).where(tenants.TelegramChat.is_active == True)
        return await self.get_all(stmt)

    async def create_chat(self, schema: schemas.TelegramChatCreateSchema) -> tenants.TelegramChat:
        return await self.save(model=tenants.TelegramChat, schema=schema)

    async def update_chat(self, pk: int, schema: schemas.TelegramChatUpdateSchema) -> tenants.TelegramChat:
        obj = await self.get_object_or_404(
            select(tenants.TelegramChat).where(tenants.TelegramChat.id == pk)
        )
        return await self.update(obj=obj, schema=schema)

    async def delete_chat(self, pk: int) -> dict:
        obj = await self.get_object_or_404(
            select(tenants.TelegramChat).where(tenants.TelegramChat.id == pk)
        )
        await self.update(obj=obj, is_active=False)
        return self.success


monthly_trans_service = MonthlyTransactionService.annotated('db')
tenant_service = TenantService.annotated('db')
tenant_detail_service = TenantDetailService.annotated('db')
telegram_chat_service = TelegramChatService.annotated('db')