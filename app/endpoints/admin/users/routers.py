from fastapi import APIRouter

from . import schemas
from .services import user_service, seller_detail_service

router = APIRouter(prefix="/sellers")

seller_tag = ["Admin | Sellers"]
seller_detail_tag = ["Admin | Sellers Detail"]


@router.post('/create/', tags=seller_tag)
async def seller_create(schema: schemas.SellerCreateSchema, service: user_service):
    return await service.create_seller(schema)


@router.get('/list/', tags=seller_tag)
async def get_all_sellers(service: user_service):
    return await service.sellers_list()


@router.get('/{seller_id}/', tags=seller_detail_tag)
async def get_seller_detail(seller_id: int, service: seller_detail_service):
    return await service.seller_detail(seller_id=seller_id)


@router.patch('/{seller_id}/', tags=seller_tag)
async def seller_update(seller_id: int, schema: schemas.SellerUpdateSchema, service: user_service):
    return await service.update_seller(seller_id=seller_id, schema=schema)


@router.delete('/{seller_id}/', tags=seller_tag)
async def seller_delete(seller_id: int, service: user_service):
    return await service.delete_seller(seller_id=seller_id)


# ---------- seller detail apis ---------
@router.patch('/monthly-trans/{pk}/', tags=seller_detail_tag)
async def update_monthly_trans(pk: int, schema: schemas.MonthlyTransUpdateSchema, service: seller_detail_service):
    return await service.update_monthly_trans(pk=pk, schema=schema)


@router.get('/{seller_id}/tenants/', tags=seller_detail_tag)
async def get_seller_tenants(seller_id: int, service: seller_detail_service):
    return await service.seller_tenants(seller_id=seller_id)

