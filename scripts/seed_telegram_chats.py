"""
Mavjud Tenant lar uchun bittadan TelegramChat va MessageHistory qo'shadi.

Foydalanish:
  python scripts/seed_telegram_chats.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.settings import settings
from app.models.tenants.tenant import Tenant
from app.models.tenants.telegram_chat import TelegramChat, MessageHistory
from app.models.users.user import User


async def seed():
    engine = create_async_engine(settings.DATABASE_URL)
    Session = async_sessionmaker(engine, expire_on_commit=False)

    async with Session() as session:
        tenants = (await session.scalars(select(Tenant))).all()
        if not tenants:
            print("[XATO] DB da hech qanday Tenant topilmadi.")
            await engine.dispose()
            return

        sender = await session.scalar(select(User))
        if not sender:
            print("[XATO] DB da hech qanday User topilmadi.")
            await engine.dispose()
            return

        for tenant in tenants:
            existing_chat = await session.scalar(
                select(TelegramChat).where(
                    TelegramChat.core_tenant_id == tenant.core_tenant_id
                )
            )
            if existing_chat:
                print(f"[SKIP] Tenant id={tenant.id} uchun TelegramChat allaqachon mavjud.")
                continue

            chat = TelegramChat(
                name=f"Tenant-{tenant.core_tenant_id} Chat",
                chat_id=-(1001000000000 + tenant.core_tenant_id),
                message_thread_id=0,
                is_active=True,
                core_tenant_id=tenant.core_tenant_id,
            )
            session.add(chat)
            await session.flush()

            message = MessageHistory(
                chat_id=chat.id,
                sender_id=sender.id,
                message=f"Tenant {tenant.core_tenant_id} uchun boshlang'ich xabar.",
                is_delivered=True,
            )
            session.add(message)
            print(f"[OK] Tenant id={tenant.id}, core_tenant_id={tenant.core_tenant_id} => TelegramChat id={chat.id} + MessageHistory yaratildi.")

        await session.commit()
        print("\n[DONE] Seed muvaffaqiyatli yakunlandi.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())