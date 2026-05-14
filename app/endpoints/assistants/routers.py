from fastapi import APIRouter

from app.endpoints.assistants.services import supers_service

router = APIRouter(prefix="/assistants", tags=["assistants"])


@router.get('/{seller_id}/')
async def get_supervisors_by_seller_id(seller_id: int, service: supers_service):
    return await service.get_supervisors_by_seller_id(seller_id)






