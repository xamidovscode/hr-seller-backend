from sqlalchemy import select

from app.models import TelegramChat
from app.resources.services import BaseService
from . import schemas


class TelegramChatService(BaseService):

    async def create_chat(self, schema: schemas.TelegramChatCreateSchema) -> TelegramChat:
        return await self.save(model=TelegramChat, schema=schema)

    async def update_chat(self, pk: int, schema: schemas.TelegramChatUpdateSchema) -> TelegramChat:
        obj = await self.get_object_or_404(
            select(TelegramChat).where(TelegramChat.id == pk)
        )
        return await self.update(obj=obj, schema=schema)

    async def delete_chat(self, pk: int) -> dict:
        obj = await self.get_object_or_404(
            select(TelegramChat).where(TelegramChat.id == pk)
        )
        await self.update(obj=obj, is_active=False)
        return self.success

    async def tenant_chats(self, core_tenant_id: int) -> list:
        return await self.get_all(
            select(TelegramChat)
            .where(TelegramChat.core_tenant_id == core_tenant_id)
        )


telegram_chat_service = TelegramChatService.annotated('db')
