from fastapi import APIRouter

from .schemas import TenantCreateSchema, TenantUpdateSchema, TelegramChatCreateSchema, TelegramChatUpdateSchema
from .services import tenant_service, telegram_chat_service

tenants_router = APIRouter(prefix="/tenants", tags=["Admin | Tenants"])
tenant_detail_router = APIRouter(prefix="/tenants", tags=["Admin | Tenant Detail"])
telegram_chat_router = APIRouter(prefix="/telegram-chats", tags=["Admin | Telegram Chats"])


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