from fastapi import APIRouter

from .schemas import TenantCreateSchema, TenantUpdateSchema
from .services import tenant_service

tenants_router = APIRouter(prefix="/tenants", tags=["Admin | Tenants"])
tenant_detail_router = APIRouter(prefix="/tenants", tags=["Admin | Tenant Detail"])


@tenants_router.get('/all/')
async def get_all_tenants(service: tenant_service):
    return await service.get_all_tenants()


@tenants_router.post('/create/')
async def create_tenant(service: tenant_service, schema: TenantCreateSchema):
    return await service.create_tenant(schema)


@tenants_router.get('/statistics/')
async def get_tenant_statistics(service: tenant_service):
    return await service.tenant_statistics()


@tenants_router.patch('/{core_tenant_id}/')
async def update_tenant(core_tenant_id: int, service: tenant_service, schema: TenantUpdateSchema):
    return await service.tenant_update(core_tenant_id=core_tenant_id, schema=schema)

