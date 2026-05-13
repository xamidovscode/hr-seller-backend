from fastapi import APIRouter

from app.endpoints.tenants.services import tenant_service

router = APIRouter(prefix='/tenants', tags=["tenants"])

@router.get('/all/')
async def get_all_tenants(service: tenant_service):
    return await service.get_all_tenants()

