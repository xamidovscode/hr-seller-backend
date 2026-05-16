"""
Foydalanish:
  python scripts/create_user.py seller --username john --full-name "John Doe" --password secret --percentage 10 --duration 6
  python scripts/create_user.py admin  --username admin1 --full-name "Admin User" --password secret
"""
import asyncio
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.settings import settings
from app.models.users.user import User
from app.models.choices import UserRoles
from app.utils.jwt import hash_password


async def create_user(
    role: UserRoles,
    username: str,
    full_name: str,
    password: str,
    phone: str | None = None,
    percentage: float = 0,
    duration: int = 0,
):
    engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    )
    Session = async_sessionmaker(engine, expire_on_commit=False)

    async with Session() as session:
        existing = await session.scalar(select(User).where(User.username == username))
        if existing:
            print(f"[XATO] '{username}' username allaqachon mavjud!")
            await engine.dispose()
            return

        user = User(
            username=username,
            full_name=full_name,
            password=hash_password(password),
            phone=phone,
            role=role,
            is_active=True,
            percentage=percentage,
            duration=duration,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"[OK] {role.value.capitalize()} yaratildi: id={user.id}, username={user.username}")

    await engine.dispose()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=["seller", "admin", "super_admin"])
    parser.add_argument("--username", required=True)
    parser.add_argument("--full-name", required=True, dest="full_name")
    parser.add_argument("--password", required=True)
    parser.add_argument("--phone", default=None)
    parser.add_argument("--percentage", type=float, default=0)
    parser.add_argument("--duration", type=int, default=0)

    args = parser.parse_args()

    asyncio.run(create_user(
        role=UserRoles(args.role),
        username=args.username,
        full_name=args.full_name,
        password=args.password,
        phone=args.phone,
        percentage=args.percentage,
        duration=args.duration,
    ))


if __name__ == "__main__":
    main()