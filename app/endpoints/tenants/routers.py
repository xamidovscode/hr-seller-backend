from fastapi import APIRouter

from app.endpoints.tenants.schemas import TenantCreateSchema
from app.endpoints.tenants.services import tenant_service

router = APIRouter(prefix='/tenants', tags=["tenants"])

@router.get('/all/')
async def get_all_tenants(service: tenant_service):
    return await service.get_all_tenants()


@router.post('/create/')
async def create_tenant(service: tenant_service, schema: TenantCreateSchema):
    return await service.create_tenant(schema)

