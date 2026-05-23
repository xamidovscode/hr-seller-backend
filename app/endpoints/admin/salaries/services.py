from app.resources.services import BaseService
from app.resources.services.grpc.salaries import SalaryGrpcClient

_salary_grpc_client = SalaryGrpcClient()


class SalaryService(BaseService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._salary_grpc_client = _salary_grpc_client

    async def salaries_list(self):
        return await self._salary_grpc_client.salaries_list()

    async def salary_employees(self, salary_id: int):
        return await self._salary_grpc_client.salary_employees(salary_id=salary_id)


salary_service = SalaryService.annotated('db')