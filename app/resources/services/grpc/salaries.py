from app.core.settings import settings
from app.resources.services.base.grpc_base import GrpcClient
from app.resources.grpc.salaries.stubs import salaries_pb2, salaries_pb2_grpc


class SalaryGrpcClient(GrpcClient):

    @property
    def host(self) -> str:
        return settings.HR_CORE_GRPC_HOST

    def _create_stub(self, channel):
        return salaries_pb2_grpc.SalaryServiceStub(channel)

    async def salaries_list(self):
        stub = await self._get_stub()
        response = await stub.GetGroupedSalaries(salaries_pb2.GroupedSalariesRequest())
        return self._message_to_dict(response)

    async def salary_employees(self, salary_id: int):
        stub = await self._get_stub()
        response = await stub.GetSalaryEmployees(salaries_pb2.SalaryEmployeesRequest(salary_id=salary_id))
        return self._message_to_dict(response)
