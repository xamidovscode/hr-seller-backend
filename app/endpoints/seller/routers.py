from fastapi import APIRouter, Depends, HTTPException

from app.endpoints.seller.services import seller_service
from app.models.choices import UserRoles
from app.resources.permissions.dependencies import require_roles

router = APIRouter(tags=["Seller"])

_seller = [Depends(require_roles(UserRoles.seller))]


@router.get('/tenants/', dependencies=_seller)
async def get_seller_tenants(service: seller_service):
    return await service.get_seller_tenants()


@router.get('/assistants/', dependencies=_seller)
async def get_seller_assistants(service: seller_service):
    return await service.get_seller_assistants()

