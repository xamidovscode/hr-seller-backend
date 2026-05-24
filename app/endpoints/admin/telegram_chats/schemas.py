from typing import Optional

from pydantic import BaseModel


class TelegramChatCreateSchema(BaseModel):
    name: str
    chat_id: int
    message_thread_id: int = 0
    is_active: bool = True
    core_tenant_id: int


class TelegramChatUpdateSchema(BaseModel):
    name: Optional[str] = None
    chat_id: Optional[int] = None
    message_thread_id: Optional[int] = None
    is_active: Optional[bool] = None
    core_tenant_id: Optional[int] = None
