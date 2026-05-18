from fastapi import APIRouter, Depends

from . import schemas
from .services import user_service
from ...models.choices import UserRoles
from ...resources.permissions.dependencies import require_roles

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    '/create/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    response_model=schemas.SellerCreateResponseSchema
)
async def seller_create(schema: schemas.SellerCreateSchema, service: user_service):
    return await service.create_user(schema)


@router.get('/list/', dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))])
async def get_all_sellers(service: user_service):
    return await service.sellers_list()


@router.get('/{seller_id}/', dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))])
async def seller_detail(seller_id: int, service: user_service):
    return await service.seller_detail(seller_id=seller_id)


@router.patch(
    '/{seller_id}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
)
async def seller_update(seller_id: int, schema: schemas.SellerUpdateSchema, service: user_service):
    return await service.update_seller(seller_id=seller_id, schema=schema)


@router.delete(
    '/{seller_id}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
)
async def seller_delete(seller_id: int, service: user_service):
    return await service.delete_seller(seller_id=seller_id)

