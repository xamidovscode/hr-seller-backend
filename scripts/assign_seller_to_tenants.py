"""
Barcha tenantlarning seller_id sini 4 ga o'rnatadi.

Foydalanish:
  python scripts/assign_seller_to_tenants.py
  python scripts/assign_seller_to_tenants.py --seller-id 7   # boshqa seller
  python scripts/assign_seller_to_tenants.py --dry-run        # faqat ko'rish
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.settings import settings
from app.models.tenants.tenant import Tenant
from app.models import User


async def assign(seller_id: int, dry_run: bool) -> None:
    engine = create_async_engine(settings.DATABASE_URL)
    Session = async_sessionmaker(engine, expire_on_commit=False)

    async with Session() as session:
        seller = await session.scalar(select(User).where(User.id == seller_id))
        if seller is None:
            print(f"[ERROR] id={seller_id} li seller topilmadi.")
            return

        print(f"[INFO] Seller: {seller.id} — {getattr(seller, 'username', seller.id)}")

        tenants = (await session.scalars(select(Tenant))).all()
        already = [t for t in tenants if t.seller_id == seller_id]
        to_update = [t for t in tenants if t.seller_id != seller_id]

        print(f"[INFO] Jami tenant: {len(tenants)}")
        print(f"[INFO] Allaqachon seller_id={seller_id}: {len(already)} ta")
        print(f"[INFO] O'zgartiriladi: {len(to_update)} ta")

        if dry_run:
            for t in to_update:
                print(f"  [DRY-RUN] Tenant id={t.id} core_tenant_id={t.core_tenant_id} "
                      f"seller_id: {t.seller_id} -> {seller_id}")
            print("[DRY-RUN] Hech narsa saqlanmadi.")
            return

        if to_update:
            ids = [t.id for t in to_update]
            await session.execute(
                update(Tenant).where(Tenant.id.in_(ids)).values(seller_id=seller_id)
            )
            await session.commit()
            print(f"[DONE] {len(to_update)} ta tenant seller_id={seller_id} ga o'rnatildi.")
        else:
            print("[DONE] O'zgartiriladigan tenant yo'q.")

    await engine.dispose()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--seller-id", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    asyncio.run(assign(seller_id=args.seller_id, dry_run=args.dry_run))