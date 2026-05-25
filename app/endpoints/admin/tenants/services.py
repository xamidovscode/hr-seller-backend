from decimal import Decimal

from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.settings import settings
from app.models import (
    Tenant,
    TelegramChat,
    MessageHistory,
    User,
)
from app.models.choices import TenantTypes
from app.resources.services import BaseService, TenantGrpcClient, TenantPlansGrpcClient
from app.utils.time import now
from . import schemas

_tenant_grpc = TenantGrpcClient()
_tenant_plans_grpc = TenantPlansGrpcClient()


class TenantService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = _tenant_grpc

    async def get_all_tenants(self):
        local_tenants = await self.get_all(
            select(Tenant).options(selectinload(Tenant.seller))
        )
        core_tenants = await self._tenant_grpc.get_tenants()

        local_tenant_data = {
            tenant.core_tenant_id: {
                'id': tenant.id,
                'type': tenant.type,
                'from_date': tenant.from_date,
                'to_date': tenant.to_date,
                'percentage': tenant.percentage,
                'seller_id': tenant.seller_id,
                'seller_full_name': tenant.seller.full_name if tenant.seller else None,
            }
            for tenant in local_tenants
        }

        return [
            {
                **tenant,
                'tenant_type': "imb_hr",
                "seller_info": local_tenant_data.get(tenant['id'], {}),
            }
            for tenant in core_tenants
        ]

    @property
    def _auth_headers(self) -> dict:
        return {'X-Api-Secret-Key': settings.HR_API_SECRET_KEY}

    async def create_tenant(self, schema: schemas.TenantCreateSchema):
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenants/'
        data = schema.model_dump(mode='json')

        seller_id = data.pop('seller_id', None)

        async with self.atomic():
            if seller_id:
                seller = await self.get_object_or_404(
                    select(User).where(User.id == seller_id)
                )
                tenant = await self.save(
                    model=Tenant,
                    core_tenant_id=0,
                    type=TenantTypes.IMB_HR,
                    from_date=now().date(),
                    to_date=now().date() + relativedelta(months=seller.duration),
                    percentage=seller.percentage,
                    seller=seller,
                )
            else:
                tenant = await self.save(
                    model=Tenant,
                    core_tenant_id=0,
                    type=TenantTypes.IMB_HR,
                    from_date=now().date(),
                    to_date=now().date(),
                    percentage=Decimal("0.00"),
                )

            response = await self.httpx_post(url=url, data=data, headers=self._auth_headers)
            await self.update(obj=tenant, core_tenant_id=response['id'])

        return response

    async def tenant_update(self, core_tenant_id: int, schema: schemas.TenantUpdateSchema):
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenants/{core_tenant_id}/'
        data = schema.model_dump(mode='json')
        response = await self.httpx_patch(url=url, data=data, headers=self._auth_headers)
        return response

    async def tenant_statistics(self):
        hr_stats = await self._tenant_grpc.get_tenants_balance_status(ids=[])
        return {
            'imb_hr': hr_stats,
            'imb_edu': {
                'must_paid_amount': Decimal('0.00'),
                'not_paid_amount': Decimal('0.00'),
                'paid_amount': Decimal('0.00'),
            }
        }


class TenantDetailService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = _tenant_grpc
        self._tenant_plans_grpc = _tenant_plans_grpc

    async def tenant_detail(self, core_tenant_id: int):
        core_tenant_data = await self._tenant_grpc.get_tenant_by_id(pk=core_tenant_id)
        return core_tenant_data

    async def get_active_plans(self, core_tenant_id: int):
        return await self._tenant_plans_grpc.get_tenant_active_plan(tenant_id=core_tenant_id)

    async def get_my_data(self, core_tenant_id: int):
        return await self._tenant_plans_grpc.get_tenant_my_data(tenant_id=core_tenant_id)

    async def get_transactions(self, core_tenant_id: int):
        return await self._tenant_plans_grpc.get_tenant_transactions(tenant_id=core_tenant_id)

    async def get_transactions_detail(self, core_tenant_id: int, date: str = ''):
        return await self._tenant_plans_grpc.get_tenant_transactions_detail(tenant_id=core_tenant_id, date=date)

    async def get_telegram_chats(self, core_tenant_id: int):
        stmt = (
            select(TelegramChat)
            .where(
                TelegramChat.is_active == True,
                TelegramChat.core_tenant_id == core_tenant_id,
            )
        )
        return await self.get_all(stmt)

    async def get_messages_history(self, core_tenant_id: int):
        stmt = (
            select(MessageHistory)
            .join(TelegramChat, MessageHistory.chat_id == TelegramChat.id)
            .where(
                TelegramChat.core_tenant_id == core_tenant_id
            )
        )
        return await self.get_all(stmt)

    @property
    def _auth_headers(self) -> dict:
        return {'X-Api-Secret-Key': settings.HR_API_SECRET_KEY}

    async def update_active_plan(self, core_tenant_id: int, schema: schemas.ActivePlanUpdateSchema) -> dict:
        tenant_data = await self._tenant_grpc.get_tenant_by_id(pk=core_tenant_id)
        schema_name = tenant_data['schema_name']
        url = f'{settings.HR_CORE_URL}/api/v1/common/tenant-plans/active-plan/update/'
        headers = {**self._auth_headers, 'Tenant': schema_name}
        data = schema.model_dump(mode='json')
        return await self.httpx_post(url=url, data=data, headers=headers)


tenant_service = TenantService.annotated('db')
tenant_detail_service = TenantDetailService.annotated('db')