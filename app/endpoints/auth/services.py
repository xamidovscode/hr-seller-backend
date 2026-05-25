from sqlalchemy import select

from app.resources import BaseService, TenantPlansGrpcClient
from . import schemas
from app.models import User
from app.utils import BadRequest, verify_password, create_access_token
from ...models.choices import UserRoles
from ...resources.seller.seller_balance_calculator import SellerBalanceCalculator

_tenant_plans_grpc = TenantPlansGrpcClient()


class AuthService(BaseService):
    user: User

    async def login(self, schema: schemas.LoginSchema):

        user = await self.get_object_or_none(
            select(User).where(
                User.is_active == True, User.username == schema.username,
            )
        )

        if not user:
            raise BadRequest({
                "msg": "Foydalanuvchi topilmadi!",
            })

        if not verify_password(schema.password, user.password):
            raise BadRequest({
                'msg': 'Xato parol kiritildi!'
            })

        return {
            'user_id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'phone': user.phone,
            'is_active': user.is_active,
            'access_token': create_access_token(user),
        }

    async def get_profile(self):
        user = self.user
        data = {
            'user_id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'phone': user.phone,
            'is_active': user.is_active,
            'role': user.role,
        }
        return data

