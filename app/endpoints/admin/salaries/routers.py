from fastapi import APIRouter
from .services import salary_service
router = APIRouter(prefix="/salaries", tags=["Admin | Salaries"])

@router.get('/list/')
async def get_salaries_list(service: salary_service):
    return await service.salaries_list()


