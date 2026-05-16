from fastapi import APIRouter, Depends, HTTPException

from app.endpoints.seller.services import seller_service
from app.models.choices import UserRoles
from app.resources.permissions.dependencies import require_roles

router = APIRouter(prefix='/sellers', tags=['seller'])


@router.get('/tenants/', dependencies=[Depends(require_roles(UserRoles.seller,))])
async def get_tenants(service: seller_service):
    return await service.get_seller_tenants()



@router.get('/assistants/', dependencies=[Depends(require_roles(UserRoles.seller,))])
async def get_tenants(service: seller_service):
    return await service.get_seller_assistants()

