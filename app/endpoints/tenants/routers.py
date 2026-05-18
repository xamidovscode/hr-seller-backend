from fastapi import APIRouter, Depends

from app.endpoints.tenants.schemas import (
    TenantCreateSchema, TenantUpdateSchema,
    MonthlyTransactionCreateSchema, MonthlyTransactionUpdateSchema,
)
from app.endpoints.tenants.services import tenant_service, monthly_trans_service
from app.models.choices import UserRoles
from app.resources.permissions.dependencies import require_roles

router = APIRouter(prefix='/tenants', tags=["tenants"])

@router.get(
    '/all/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))]
)
async def get_all_tenants(service: tenant_service):
    return await service.get_all_tenants()


@router.post(
    '/create/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))]
)
async def create_tenant(service: tenant_service, schema: TenantCreateSchema):
    return await service.create_tenant(schema)


@router.get(
    '/{core_tenant_id}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))]
)
async def get_tenant_detail(core_tenant_id: int, service: tenant_service):
    return await service.tenant_detail(core_tenant_id=core_tenant_id)


@router.patch(
    '/{tenant_id}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))]
)
async def update_tenant(tenant_id: int, service: tenant_service, schema: TenantUpdateSchema):
    return await service.tenant_update(tenant_id=tenant_id, schema=schema)


@router.post(
    '/monthly-transactions/create/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
)
async def create_monthly_transaction(schema: MonthlyTransactionCreateSchema, service: monthly_trans_service):
    return await service.create_transaction(schema=schema)


@router.patch(
    '/monthly-transactions/{pk}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
)
async def update_monthly_transaction(pk: int, schema: MonthlyTransactionUpdateSchema, service: monthly_trans_service):
    return await service.update_transaction(pk=pk, schema=schema)


@router.delete(
    '/monthly-transactions/{pk}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
)
async def delete_monthly_transaction(pk: int, service: monthly_trans_service):
    return await service.delete_transaction(pk=pk)



