from fastapi import APIRouter, Query
from typing import Optional

from .schemas import TenantCreateSchema, TenantUpdateSchema, ActivePlanUpdateSchema
from .services import tenant_service, tenant_detail_service

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


@tenant_detail_router.get('/{core_tenant_id}/detail/')
async def get_tenant_detail(core_tenant_id: int, service: tenant_detail_service):
    return await service.tenant_detail(core_tenant_id=core_tenant_id)


@tenant_detail_router.get('/{core_tenant_id}/my-data/')
async def get_tenant_my_data(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_my_data(core_tenant_id=core_tenant_id)


@tenant_detail_router.get('/{core_tenant_id}/active-plan/')
async def get_tenant_active_plan(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_active_plans(core_tenant_id=core_tenant_id)


@tenant_detail_router.get('/{core_tenant_id}/transactions/')
async def get_tenant_transactions(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_transactions(core_tenant_id=core_tenant_id)


@tenant_detail_router.get('/{core_tenant_id}/transactions-detail/')
async def get_tenant_transactions_detail(
    core_tenant_id: int,
    service: tenant_detail_service,
    date: Optional[str] = Query(default=None, description="Filter by month: YYYY-MM-DD"),
):
    return await service.get_transactions_detail(core_tenant_id=core_tenant_id, date=date or '')


@tenant_detail_router.post('/{core_tenant_id}/active-plan/update/')
async def update_tenant_active_plan(
    core_tenant_id: int,
    service: tenant_detail_service,
    schema: ActivePlanUpdateSchema,
):
    return await service.update_active_plan(core_tenant_id=core_tenant_id, schema=schema)