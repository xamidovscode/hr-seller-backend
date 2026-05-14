from fastapi import APIRouter

from app.endpoints.supervisor.services import supers_service

router = APIRouter(prefix="/assistants/", tags=["supervisor"])


@router.get('/{seller_id}/')
async def get_supervisors_by_seller_id(seller_id: int, service: supers_service):
    return await supers_service.get_supervisors_by_seller_id(seller_id)

