import asyncio

from fastapi import APIRouter
from app.resources.grpc.client import get_tenants

router = APIRouter(prefix='/tenants', tags=["tenants"])

@router.get('/all/')
async def root():
    tenants = await asyncio.to_thread(get_tenants)
    return [
        {
            "id": tenant.id,
            "name": tenant.name,
            "schema_name": tenant.schema_name,
        }
        for tenant in tenants
    ]
