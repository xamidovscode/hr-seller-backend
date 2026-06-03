from fastapi import APIRouter

from .schemas import TelegramChatCreateSchema, TelegramChatUpdateSchema
from .services import telegram_chat_service

router = APIRouter(prefix="/telegram-chats", tags=["Admin | Telegram Chats"])


@router.post('/create/')
async def create_telegram_chat(schema: TelegramChatCreateSchema, service: telegram_chat_service):
    return await service.create_chat(schema=schema)


@router.patch('/{pk}/')
async def update_telegram_chat(pk: int, schema: TelegramChatUpdateSchema, service: telegram_chat_service):
    return await service.update_chat(pk=pk, schema=schema)


@router.delete('/{pk}/')
async def delete_telegram_chat(pk: int, service: telegram_chat_service):
    return await service.delete_chat(pk=pk)


@router.delete('/{pk}/')
async def tenant_telegram_chat(core_tenant_id: int, service: telegram_chat_service):
    return await service.tenant_chats(core_tenant_id=core_tenant_id)


