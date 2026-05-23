from fastapi import APIRouter

from app.endpoints.seller.services import seller_service

router = APIRouter(tags=["Seller"])


@router.get('/tenants/')
async def get_seller_tenants(service: seller_service):
    return await service.get_seller_tenants()


@router.get('/assistants/')
async def get_seller_assistants(service: seller_service):
    return await service.get_seller_assistants()

