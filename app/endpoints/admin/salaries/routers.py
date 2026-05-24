from fastapi import APIRouter
from .schemas import GroupedSalaryListSchema, SalaryEmployeeListSchema
from .services import salary_service

router = APIRouter(prefix="/salaries", tags=["Admin | Salaries"])


@router.get('/list/', response_model=GroupedSalaryListSchema)
async def get_salaries_list(service: salary_service):
    return await service.salaries_list()


@router.get('/{salary_id}/employees/', response_model=SalaryEmployeeListSchema)
async def get_salary_employees(salary_id: int, service: salary_service):
    return await service.salary_employees(salary_id=salary_id)
