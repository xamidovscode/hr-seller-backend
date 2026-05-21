from fastapi import APIRouter, Depends

from app.models.choices import UserRoles
from app.resources.permissions.dependencies import require_roles
from .schemas import TenantCreateSchema, TenantUpdateSchema, MonthlyTransactionCreateSchema, MonthlyTransactionUpdateSchema, TelegramChatCreateSchema, TelegramChatUpdateSchema
from .services import tenant_service, monthly_trans_service, tenant_detail_service, telegram_chat_service

_admin = [Depends(require_roles(UserRoles.admin, UserRoles.super_admin))]

tenants_router = APIRouter(prefix="/tenants", tags=["Admin | Tenants"], dependencies=_admin)
tenant_detail_router = APIRouter(prefix="/tenants", tags=["Admin | Tenant Detail"], dependencies=_admin)
monthly_trans_router = APIRouter(prefix="/tenants", tags=["Admin | Monthly Transactions"], dependencies=_admin)
telegram_chat_router = APIRouter(prefix="/telegram-chats", tags=["Admin | Telegram Chats"], dependencies=_admin)


# ---------- tenants crud ----------
@tenants_router.get('/all/')
async def get_all_tenants(service: tenant_service):
    return await service.get_all_tenants()


@tenants_router.post('/create/')
async def create_tenant(service: tenant_service, schema: TenantCreateSchema):
    return await service.create_tenant(schema)


@tenants_router.patch('/{core_tenant_id}/')
async def update_tenant(core_tenant_id: int, service: tenant_service, schema: TenantUpdateSchema):
    return await service.tenant_update(core_tenant_id=core_tenant_id, schema=schema)


# ---------- tenant detail ----------
@tenant_detail_router.get('/{core_tenant_id}/')
async def get_tenant_detail(core_tenant_id: int, service: tenant_detail_service):
    return await service.tenant_detail(core_tenant_id=core_tenant_id)


@tenant_detail_router.get('/{core_tenant_id}/active-plan/')
async def get_tenant_active_plans(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_active_plans(core_tenant_id=core_tenant_id)


@tenant_detail_router.get('/{core_tenant_id}/monthly-transactions/')
async def get_tenant_monthly_transactions(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_monthly_transactions(core_tenant_id=core_tenant_id)


@tenant_detail_router.get('/{core_tenant_id}/telegram-chats/')
async def get_tenant_telegram_chats(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_telegram_chats(core_tenant_id=core_tenant_id)


@tenant_detail_router.get('/{core_tenant_id}/message-history/')
async def get_tenant_messages_history(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_messages_history(core_tenant_id=core_tenant_id)


# ---------- monthly transactions ----------
@monthly_trans_router.post('/monthly-transactions/create/')
async def create_monthly_transaction(schema: MonthlyTransactionCreateSchema, service: monthly_trans_service):
    return await service.create_transaction(schema=schema)


@monthly_trans_router.patch('/monthly-transactions/{pk}/')
async def update_monthly_transaction(pk: int, schema: MonthlyTransactionUpdateSchema, service: monthly_trans_service):
    return await service.update_transaction(pk=pk, schema=schema)


@monthly_trans_router.delete('/monthly-transactions/{pk}/')
async def delete_monthly_transaction(pk: int, service: monthly_trans_service):
    return await service.delete_transaction(pk=pk)


# ---------- telegram chats ----------
@telegram_chat_router.post('/create/')
async def create_telegram_chat(schema: TelegramChatCreateSchema, service: telegram_chat_service):
    return await service.create_chat(schema=schema)


@telegram_chat_router.patch('/{pk}/')
async def update_telegram_chat(pk: int, schema: TelegramChatUpdateSchema, service: telegram_chat_service):
    return await service.update_chat(pk=pk, schema=schema)


@telegram_chat_router.delete('/{pk}/')
async def delete_telegram_chat(pk: int, service: telegram_chat_service):
    return await service.delete_chat(pk=pk)