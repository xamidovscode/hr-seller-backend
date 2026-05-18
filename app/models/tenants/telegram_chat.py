from typing import TYPE_CHECKING
from sqlalchemy import Integer, Boolean, String, ForeignKey, BigInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import BaseModel


if TYPE_CHECKING:
    from app.models import User

class TelegramChat(BaseModel):
    __tablename__ = "tenant_tg_chat"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Telegram chat name",
    )
    chat_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Telegram chat id",
    )
    message_thread_id: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default='0',
        comment="Super chats topic id",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default='false',
        comment="Is active?",
    )

    core_tenant_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Core service client id",
    )

    tg_messages_history: Mapped[list['MessageHistory']] = relationship(
        back_populates="chat",
    )


class MessageHistory(BaseModel):
    __tablename__ = "tg_chat_message_history"

    chat_id: Mapped[int] = mapped_column(
        ForeignKey('tenant_tg_chat.id', ondelete="CASCADE"),
    )
    chat: Mapped['TelegramChat'] = relationship(
        back_populates="tg_messages_history",
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"),
    )
    sender: Mapped['User'] = relationship(
        back_populates="sent_messages",
    )

    message: Mapped[str] = mapped_column(
        String(555),
        nullable=False,
        comment="Sent message body",
    )
    is_delivered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="Is delivered?",
    )
    tg_response: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        comment="Telegram API response payload",
    )





