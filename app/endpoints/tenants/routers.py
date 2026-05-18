from fastapi import APIRouter, Depends

from app.endpoints.tenants.schemas import (
    TenantCreateSchema,
    TenantUpdateSchema,
    MonthlyTransactionCreateSchema,
    MonthlyTransactionUpdateSchema,
)
from app.endpoints.tenants.services import (
    tenant_service,
    monthly_trans_service,
    tenant_detail_service,
)
from app.models.choices import UserRoles
from app.resources.permissions.dependencies import require_roles

router = APIRouter(prefix='/tenants')



# ---------- tenants api ----------
@router.get(
    '/all/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenants'],
)
async def get_all_tenants(service: tenant_service):
    return await service.get_all_tenants()


@router.post(
    '/create/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenants'],
)
async def create_tenant(service: tenant_service, schema: TenantCreateSchema):
    return await service.create_tenant(schema)


@router.patch(
    '/{core_tenant_id}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenants'],
)
async def update_tenant(core_tenant_id: int, service: tenant_service, schema: TenantUpdateSchema):
    return await service.tenant_update(core_tenant_id=core_tenant_id, schema=schema)





# ---------- tenant detail apis ----------
@router.get(
    '/{core_tenant_id}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenant-detail'],
)
async def get_tenant_detail(core_tenant_id: int, service: tenant_detail_service):
    return await service.tenant_detail(core_tenant_id=core_tenant_id)


@router.get(
    '/{core_tenant_id}/active-plan/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenant-detail'],
)
async def get_tenant_active_plans(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_active_plans(core_tenant_id=core_tenant_id)


@router.get(
    '/{core_tenant_id}/monthly-transactions/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenant-detail'],
)
async def get_tenant_active_plans(core_tenant_id: int, service: tenant_detail_service):
    return await service.get_monthly_transactions(core_tenant_id=core_tenant_id)



# ---------- monthly transactions ----------
@router.post(
    '/monthly-transactions/create/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenant-monthly-trans'],
)
async def create_monthly_transaction(schema: MonthlyTransactionCreateSchema, service: monthly_trans_service):
    return await service.create_transaction(schema=schema)


@router.patch(
    '/monthly-transactions/{pk}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenant-monthly-trans'],
)
async def update_monthly_transaction(pk: int, schema: MonthlyTransactionUpdateSchema, service: monthly_trans_service):
    return await service.update_transaction(pk=pk, schema=schema)


@router.delete(
    '/monthly-transactions/{pk}/',
    dependencies=[Depends(require_roles(UserRoles.admin, UserRoles.super_admin))],
    tags=['tenant-monthly-trans'],
)
async def delete_monthly_transaction(pk: int, service: monthly_trans_service):
    return await service.delete_transaction(pk=pk)



