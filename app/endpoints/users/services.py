from typing import List, Any

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from app.models import users, choices, tenants
from app.resources import BaseService, TenantGrpcClient
from app.utils import hash_password
from . import schemas
from ...models.choices import TransTypes
from ...resources.seller.seller_balance_calculator import SellerBalanceCalculator
from ...resources.seller.seller_balance_detail import SellerDetail
from ...utils.time import now


_tenant_grpc = TenantGrpcClient()


class UserService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tenant_grpc = _tenant_grpc

    async def sellers_list(self) -> List[dict[str, Any]]:
        sellers = await self.get_all(
            select(users.User).where(users.User.role == choices.UserRoles.seller)
        )

        calc = SellerBalanceCalculator(self.db)
        stats = await calc.bulk_breakdown([s.id for s in sellers])

        return [
            {
                'id': s.id,
                'username': s.username,
                'full_name': s.full_name,
                'phone': s.phone,
                'percentage': s.percentage,
                'duration': s.duration,
                'is_active': s.is_active,
                **stats[s.id],
            }
            for s in sellers
        ]

    async def create_user(self, schema: schemas.SellerCreateSchema) -> users.User:

        data = schema.model_copy(
            update={
                'password': hash_password(schema.password),
                'role': choices.UserRoles.seller
            }
        ).model_dump()
        supervisor_data = data.pop("supervisor", None)

        existing = await self.get_object_or_none(
            select(users.User).where(users.User.username == data['username'])
        )

        if existing:
            raise self.error("Bu username band!")

        async with self.atomic():
            seller = await self.save(model=users.User, **data)

            if supervisor_data:
                super_seller = await self.get_object_or_404(
                    select(users.User).where(users.User.id == supervisor_data['seller_id'])
                )

                await self.save(
                    model=users.Supervisor,
                    supervisor=super_seller,
                    seller=seller,
                    from_date=now().date(),
                    to_date=now().date() + relativedelta(months=supervisor_data['duration']),
                    percentage=supervisor_data['percentage'],
                )

        return seller

    async def seller_detail(self, seller_id: int) -> Any:

        seller = await self.get_object_or_404(
            select(users.User).where(
                users.User.id == seller_id,
                users.User.role == choices.UserRoles.seller,
            )
        )

        sbd = SellerDetail(db=self.db, seller_id=seller_id)

        return {
            'id': seller.id,
            'username': seller.username,
            'full_name': seller.full_name,
            'phone': seller.phone,
            'percentage': seller.percentage,
            'duration': seller.duration,
            'is_active': seller.is_active,
            'assistants': await sbd.assistants_data(),
            'tenants': await sbd.tenants_data(tenant_grpc=self._tenant_grpc),
            'requests': await sbd.seller_requests(),
            'balance_info': await sbd.detail_balance(),
        }

    async def update_seller(self, seller_id: int, schema: schemas.SellerUpdateSchema) -> users.User:
        seller = await self.get_object_or_404(
            select(users.User).where(
                users.User.id == seller_id,
                users.User.role == choices.UserRoles.seller,
            )
        )
        return await self.update(obj=seller, schema=schema)

    async def delete_seller(self, seller_id: int) -> dict:
        seller = await self.get_object_or_404(
            select(users.User).where(
                users.User.id == seller_id,
                users.User.role == choices.UserRoles.seller,
            )
        )
        await self.update(obj=seller, is_active=False)
        return {'detail': 'Seller deactivated successfully'}

user_service = UserService.annotated('db')


