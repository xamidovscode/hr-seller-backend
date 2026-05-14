from contextlib import asynccontextmanager
from typing import Any, Iterable, Optional, Sequence
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession


class SessionMixin:
    db: AsyncSession
    _in_transaction: bool = False

    async def execute(self, stmt, *args, **kwargs) -> Result[Any]:
        return await self.db.execute(stmt, *args, **kwargs)

    async def commit(self):
        return await self.db.commit()

    async def flush(self, objects: Optional[Sequence[Any]] = None):
        return await self.db.flush(objects=objects)

    async def rollback(self):
        return await self.db.rollback()

    def add(self, obj: Any):
        return self.db.add(obj)

    def add_all(self, instances: Iterable[object]):
        return self.db.add_all(instances)

    async def merge(self, obj: Any):
        return await self.db.merge(obj)

    async def delete(self, obj: Any):
        return await self.db.delete(obj)

    async def refresh(self, obj: Any):
        return await self.db.refresh(obj)

    @asynccontextmanager
    async def atomic(self):
        async with self.db.begin_nested():
            self._in_transaction = True
            try:
                yield
            finally:
                self._in_transaction = False
        await self.commit()
