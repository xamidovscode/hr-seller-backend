"""
Core servisdan barcha tenant larni olib kelib, local DB ga sync qiladi.
Mavjud tenant lar (core_tenant_id bo'yicha) o'tkazib yuboriladi.

Foydalanish:
  python scripts/sync_tenants_from_core.py
"""
import asyncio
import sys
import os
from datetime import date
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.settings import settings
from app.models.tenants.tenant import Tenant
from app.models.choices import TenantTypes
from app.resources.services.grpc.tenant import TenantGrpcClient


async def sync():
    engine = create_async_engine(settings.DATABASE_URL)
    Session = async_sessionmaker(engine, expire_on_commit=False)
    grpc_client = TenantGrpcClient()

    print("[INFO] Core servisdan tenant lar olinmoqda...")
    core_tenants = await grpc_client.get_tenants()
    print(f"[INFO] Core da {len(core_tenants)} ta tenant topildi.")

    async with Session() as session:
        existing = (await session.scalars(select(Tenant))).all()
        existing_core_ids = {t.core_tenant_id for t in existing}

        created = 0
        skipped = 0

        for ct in core_tenants:
            core_id = ct['id']

            if core_id in existing_core_ids:
                print(f"[SKIP] core_tenant_id={core_id} allaqachon mavjud.")
                skipped += 1
                continue

            today = date.today()
            tenant = Tenant(
                core_tenant_id=core_id,
                type=TenantTypes.IMB_HR,
                from_date=today,
                to_date=today,
                percentage=Decimal("0.00"),
                seller_id=None,
            )
            session.add(tenant)
            print(f"[OK] core_tenant_id={core_id} => yangi Tenant yaratildi.")
            created += 1

        await session.commit()

    await grpc_client.close()
    await engine.dispose()

    print(f"\n[DONE] Yaratildi: {created}, O'tkazib yuborildi: {skipped}.")


if __name__ == "__main__":
    asyncio.run(sync())