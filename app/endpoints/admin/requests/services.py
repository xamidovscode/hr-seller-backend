from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import SellerRequest, User
from app.models.choices import UserRoles
from app.resources.services import BaseService
from .schemas import SellerRequestCreateSchema, SellerRequestUpdateSchema, SellerRequestFilterSchema


class SellerRequestService(BaseService):

    async def list(self, filters: SellerRequestFilterSchema) -> list[SellerRequest]:
        stmt = select(SellerRequest).options(selectinload(SellerRequest.seller))

        if filters.seller_id is not None:
            stmt = stmt.where(SellerRequest.seller_id == filters.seller_id)
        if filters.condition is not None:
            stmt = stmt.where(SellerRequest.condition == filters.condition)
        if filters.date_from is not None:
            stmt = stmt.where(SellerRequest.date >= filters.date_from)
        if filters.date_to is not None:
            stmt = stmt.where(SellerRequest.date <= filters.date_to)

        stmt = stmt.order_by(SellerRequest.date.desc())
        return await self.get_all(stmt)

    async def detail(self, pk: int) -> SellerRequest:
        return await self.get_object_or_404(
            select(SellerRequest)
            .options(selectinload(SellerRequest.seller))
            .where(SellerRequest.id == pk)
        )

    async def create(self, schema: SellerRequestCreateSchema) -> SellerRequest:
        await self.get_object_or_404(
            select(User).where(
                User.id == schema.seller_id,
                User.role == UserRoles.seller,
            )
        )
        return await self.save(model=SellerRequest, schema=schema)

    async def patch(self, pk: int, schema: SellerRequestUpdateSchema) -> SellerRequest:
        obj = await self.get_object_or_404(
            select(SellerRequest).where(SellerRequest.id == pk)
        )
        return await self.update(obj=obj, schema=schema)

    async def delete(self, pk: int) -> dict:
        obj = await self.get_object_or_404(
            select(SellerRequest).where(SellerRequest.id == pk)
        )
        return await self.remove(obj)


seller_request_service = SellerRequestService.annotated('db')
