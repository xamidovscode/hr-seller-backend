from fastapi import APIRouter

from app.endpoints.admin.plans.services import plans_service

router = APIRouter(prefix="/plans", tags=["Admin | Plans"])


# ---------- tenants crud ----------
@router.get('/list/')
async def get_plans_list(service: plans_service):
    return await service.plans_list()

