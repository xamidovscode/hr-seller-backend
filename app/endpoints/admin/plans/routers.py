from fastapi import APIRouter

from app.endpoints.admin.plans.services import plans_service
from .schemas import PlanBulkUpdateSchema

router = APIRouter(prefix="/plans", tags=["Admin | Plans"])


# ---------- tenants crud ----------
@router.get('/list/')
async def get_plans_list(service: plans_service):
    return await service.plans_list()


@router.patch('/bulk-update/')
async def plans_bulk_update(service: plans_service, schema: PlanBulkUpdateSchema):
    return await service.update_plan(schema=schema)


