import asyncio

from fastapi import APIRouter
from app.resources.grpc.client import get_tenants

router = APIRouter(prefix='/tenants', tags=["tenants"])

@router.get('/all/')
async def get_all_tenants():
    tenants = await asyncio.to_thread(get_tenants)
    result = []

    for tenant in tenants:
        result.append({
            "id": tenant.id,
            "name": tenant.name,
            "schema_name": tenant.schema_name,
            "created_on": tenant.created_on,
            "activated_at": tenant.activated_at,
            "deadline": tenant.deadline,
            "is_active": tenant.is_active,
            "on_trial": tenant.on_trial,
            "is_deleted": tenant.is_deleted,
        })

    return result
