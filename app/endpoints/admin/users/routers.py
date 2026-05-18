from fastapi import APIRouter, Depends

from app.models.choices import UserRoles
from app.resources.permissions.dependencies import require_roles
from . import schemas
from .services import user_service, seller_detail_service

router = APIRouter(prefix="/sellers")

_admin = [Depends(require_roles(UserRoles.admin, UserRoles.super_admin))]

seller_tag = ["Admin | Sellers"]
seller_detail_tag = ["Admin | Sellers Detail"]


@router.post('/create/', dependencies=_admin, tags=seller_tag)
async def seller_create(schema: schemas.SellerCreateSchema, service: user_service):
    return await service.create_seller(schema)


@router.get('/list/', dependencies=_admin, tags=seller_tag)
async def get_all_sellers(service: user_service):
    return await service.sellers_list()


@router.patch('/{seller_id}/', dependencies=_admin, tags=seller_tag)
async def seller_update(seller_id: int, schema: schemas.SellerUpdateSchema, service: user_service):
    return await service.update_seller(seller_id=seller_id, schema=schema)


@router.delete('/{seller_id}/', dependencies=_admin, tags=seller_tag)
async def seller_delete(seller_id: int, service: user_service):
    return await service.delete_seller(seller_id=seller_id)


# ---------- seller detail apis ---------
@router.get('/{seller_id}/', dependencies=_admin, tags=seller_detail_tag)
async def seller_detail(seller_id: int, service: seller_detail_service):
    return await service.seller_detail(seller_id=seller_id)


@router.get('/{seller_id}/requests/', dependencies=_admin, tags=seller_detail_tag)
async def seller_detail(seller_id: int, service: seller_detail_service):
    return await service.seller_requests(seller_id=seller_id)


@router.get('/{seller_id}/tenants/', dependencies=_admin, tags=seller_detail_tag)
async def seller_detail(seller_id: int, service: seller_detail_service):
    return await service.seller_tenants(seller_id=seller_id)


