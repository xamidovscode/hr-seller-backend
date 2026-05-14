from fastapi import APIRouter

from . import schemas
from .services import user_service

router = APIRouter(prefix="/sellers", tags=["sellers"])


@router.post('/create/', response_model=schemas.SellerCreateResponseSchema)
async def seller_create(schema: schemas.SellerCreateSchema, service: user_service):
    return await service.create_user(schema)


@router.get('/list/')
async def get_all_sellers(service: user_service):
    return await service.sellers_list()


@router.get('/{seller_id}/')
async def get_all_sellers(seller_id: int, service: user_service):
    return await service.seller_detail(seller_id=seller_id)

